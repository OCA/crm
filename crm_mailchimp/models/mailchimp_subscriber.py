# Copyright 2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MailchimpSubscriber(models.Model):
    _name = "mailchimp.subscriber"
    _description = "Mailchimp subscriber."

    def _compute_name(self):
        """Compute name from subscriber and list."""
        for this in self:
            resource = this.get_resource()
            this.name = " - ".join([this.list_id.display_name, resource.display_name])

    name = fields.Char(compute="_compute_name", store=True, readonly=True)
    list_id = fields.Many2one(
        comodel_name="mailchimp.list",
        string="Audience",
        required=True,
        ondelete="cascade",
    )
    res_model = fields.Char(
        "Resource Model",
        readonly=True,
        required=True,
        help="The database resource this attachment will be attached to.",
    )
    res_id = fields.Many2oneReference(
        "Resource ID",
        model_field="res_model",
        readonly=True,
        required=True,
        help="The record id this is attached to.",
    )
    email = fields.Char("Email", readonly=True, required=True,)
    interest_ids = fields.One2many(
        comodel_name="mailchimp.subscriber.interest",
        inverse_name="subscriber_id",
        string="Mailchimp groups",
    )
    pending_removal = fields.Boolean(
        default=False,
        help="Subscription should be deleted from Mailchimp and then unlinked.",
    )
    mailchimp_id = fields.Char(
        help="This is the mailchimp subscriber_id, based on the email address."
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Automatically set email on record, and push to mailchimp after create."""
        context = self.env.context
        for vals in vals_list:
            res_model = vals.get("res_model", context.get("default_res_model"))
            res_id = vals.get("res_id", context.get("default_res_id"))
            resource = self.env[res_model].browse(res_id)
            vals["email"] = resource.email
            vals["res_model"] = resource._name
        records = super().create(vals_list)
        records._push_to_mailchimp()
        return records

    def _push_to_mailchimp(self, vals=None):
        """Push records to Odoo. Call when resources subscribed or changed."""
        list_model = self.env["mailchimp.list"]
        model_model = self.env["mailchimp.list.model"]
        # Get mailchimp client.
        client = list_model._get_mailchimp_client()
        for this in self:
            mailchimp_list_model = model_model.search(
                [("list_id", "=", this.list_id.id), ("model", "=", this.res_model)],
                limit=1,
            )
            if not vals or mailchimp_list_model._check_push_needed(vals):
                mailchimp_list_model._push_subscriber_to_mailchimp(client, this)

    @api.model
    def get_subscriptions(self, record):
        """Utility function to return subscriber for subscribed record."""
        return self.search(
            [("res_model", "=", record._name), ("res_id", "=", record.id)]
        )

    def get_resource(self):
        """Return the actual resource linked to this subscriber."""
        self.ensure_one()
        return self.env[self.res_model].browse(self.res_id)

    @api.constrains("list_id", "mailchimp_id")
    def _check_subscriber_unique(self):
        """Within a list subscribers must be unique.

        As mailchimp_id is a translation of the email addrress, you can not
        have multiple partners (or leads etc.) with the same email address
        subscribed to the same list.
        """
        for this in self:
            existing_subscriber = self.search(
                [
                    ("list_id", "=", this.list_id.id),
                    ("email", "=", this.email),
                    ("id", "!=", this.id),
                ],
                limit=1,
            )
            if existing_subscriber:
                existing_resource = existing_subscriber.get_resource()
                subscriber_resource = this.get_resource()
                raise ValidationError(
                    _(
                        "Can not subscribe %(name)s from model %(model)s with id %(id)s"
                        " to list %(list)s.\n"
                        "Subscriber %(e_name)s from model %(e_model)s with id %(e_id)s"
                        " already subscribed with this email %(email)s"
                    )
                    % {
                        "name": subscriber_resource.display_name,
                        "model": this.res_model,
                        "id": this.res_id,
                        "list": this.list_id.display_name,
                        "e_name": existing_resource.display_name,
                        "e_model": existing_subscriber.res_model,
                        "e_id": existing_subscriber.res_id,
                        "email": this.email,
                    }
                )

    def unlink(self):
        """Make sure subscribers are removed from mailchimp first."""
        for this in self:
            if not this.mailchimp_id:
                # Subscriber never was on mailchimp, or has been succesfully removed.
                super().unlink()
                continue
            this.write({"pending_removal": True})
            this._push_to_mailchimp()
