# Copyright 2019-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

try:
    from mailchimp3.mailchimpclient import MailChimpError
except ImportError:
    MailChimpError = False


_logger = logging.getLogger(__name__)


class MailchimpListModel(models.Model):
    _name = "mailchimp.list.model"
    _description = "A mailchimp audience"

    def _compute_name(self):
        """Name is combination of list and model."""
        for this in self:
            this.name = "{}-{}".format(this.list_id.name, this.model)

    name = fields.Char(compute="_compute_name", store=True)
    list_id = fields.Many2one(
        comodel_name="mailchimp.list", required=True, ondelete="cascade",
    )
    model = fields.Char(
        required=True,
        default="res.partner",
        help="Model to link to Mailchimp."
        " Must contain email and inherit from mailchimp_subscriber_mixin.",
    )
    merge_field_ids = fields.One2many(
        comodel_name="mailchimp.merge.field",
        inverse_name="list_model_id",
        string="Merge fields",
    )
    change_trigger_fields = fields.Text(
        string="Fields that trigger push to Mailchimp",
        required=True,
        default="email, name",
        help="The fields on the model that should result in a push to Mailchimp"
        " when one or more of them are changed.\n"
        "This is a comma, separated string, and should be based on the fields"
        " used in the code of the merge fields.\n"
        "You must always include email",
    )

    @api.constrains("model")
    def _check_model(self):
        """Model must contain an email field."""
        for this in self:
            model = self.env[this.model]
            if "email" not in model._fields:
                raise ValidationError(
                    _("Model %s does not have an email field.") % model._name
                )

    @api.constrains("change_trigger_fields")
    def _check_change_trigger_fields(self):
        """Fields must exist in model, and contain email."""
        for this in self:
            model = self.env[this.model]
            email_present = False
            for fieldname in this._get_trigger_fieldnames():
                if fieldname == "email":
                    email_present = True
                if fieldname not in model._fields:
                    _logger.error(
                        _("Fieldnames %s is invalid"),
                        str(this._get_trigger_fieldnames()),
                    )
                    raise ValidationError(
                        _("Model %s does not have an %s field.")
                        % (model._name, fieldname)
                    )
            if not email_present:
                raise ValidationError(
                    _("The fieldname 'email' must be in the list of fields")
                )

    def _get_trigger_fieldnames(self):
        """Make list of the fields that should trigger change to odoo."""
        self.ensure_one()
        return [
            fieldname.strip() for fieldname in self.change_trigger_fields.split(",")
        ]

    def _check_push_needed(self, vals):
        """Check wether vals contain values that should trigger push to Mailchimp."""
        self.ensure_one()
        for fieldname in self._get_trigger_fieldnames():
            if fieldname in vals:
                return True
        return False

    def _update_from_mailchimp(self, client):
        """Update merge fields for combination of model and mailchimp audience."""
        merge_field_model = self.env["mailchimp.merge.field"]
        for this in self:
            # Update merge fields.
            merge_field_model._update_from_mailchimp(client, this)

    def _push_to_mailchimp(self, client):
        """Push aubscriber to mailchimp."""
        subscriber_model = self.env["mailchimp_subscriber"]
        for this in self:
            subscribers = subscriber_model.search(
                [("list_id", "=", this.list_id), ("res_model", "=", this.model)]
            )
            resource_model = self.env[self.model]
            for subscriber in subscribers:
                if subscriber.pending_removal:
                    this._remove_subscriber_from_mailchimp(client, subscriber)
                else:
                    resource = resource_model.browse(subscriber.res_id)
                    this._push_subscriber_to_mailchimp(client, resource)

    def _remove_subscriber_from_mailchimp(self, client, subscriber):
        """Remove subscriber from audience on mailchimp.

        Note that this might be a consequence of deleting the original resource.
        """
        self.ensure_one()
        if subscriber.mailchimp_id:
            # It might just be possible that subscriber was never pushed to mailchimp.
            try:
                client.lists.members.delete(
                    list_id=self.list_id.mailchimp_id,
                    subscriber_hash=subscriber.mailchimp_id,
                )
            except MailChimpError:
                _logger.exception(
                    "Error removing %s %s with email %s from mailchimp",
                    subscriber.res_model,
                    subscriber.display_name,
                    subscriber.email,
                )
            subscriber.write({"mailchimp_id": False})  # Will be checked in unlink()
        subscriber.unlink()

    def _push_subscriber_to_mailchimp(self, client, subscriber):
        """Add or update subscriber on mailchimp."""
        self.ensure_one()
        resource = subscriber.get_resource()
        mailchimp_data = self._get_subscriber_data(resource)
        mailchimp_data["interests"] = self._get_subscriber_interests(subscriber)
        try:
            if subscriber.mailchimp_id:
                response = client.lists.members.create_or_update(
                    list_id=self.list_id.mailchimp_id,
                    subscriber_hash=subscriber.mailchimp_id,
                    data=mailchimp_data,
                )
            else:
                response = client.lists.members.create(
                    list_id=self.list_id.mailchimp_id, data=mailchimp_data,
                )
            if subscriber.mailchimp_id != response["id"]:
                _logger.debug(
                    _("Subscriber %s has new mailchimp_id for email %s"),
                    subscriber.display_name,
                    subscriber.email,
                )
                subscriber.write({"mailchimp_id": response["id"]})
        except MailChimpError:
            _logger.exception(
                "Error pushing %s %s with email %s to mailchimp",
                resource._name,
                resource.display_name,
                resource.email,
            )

    def _get_subscriber_data(self, resource):
        """Get data from subscriber to push to Mailchimp, where code has been set."""
        self.ensure_one()
        merge_fields = {}
        for merge_field in self.merge_field_ids:
            if not merge_field.code:
                continue
            try:
                # We keep the partner key, as this will have been used in code.
                merge_fields[merge_field.tag] = safe_eval(
                    merge_field.code, {"partner": resource}, mode="eval"
                )
            except Exception:
                _logger.error(
                    _("Error getting data for merge-field %s, for resource %s"),
                    merge_field.tag,
                    resource.display_name,
                )
                raise
        data = {
            "email_address": resource.email,
            "status": "subscribed",
            "status_if_new": "subscribed",
            "merge_fields": merge_fields,
        }
        return data

    def _get_subscriber_interests(self, subscriber):
        """Get current interests for subscriber."""
        self.ensure_one()
        possible_interests = self.list_id.interest_category_ids.interest_ids
        # Pass a dictionary with all interests possible as keys and an indication
        # wether the subscriber has this interest.
        interest_dict = {
            interest.mailchimp_id: False for interest in possible_interests
        }
        for interest in subscriber.interest_ids:
            interest_dict[interest.interest_id.mailchimp_id] = True
        return interest_dict
