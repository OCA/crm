# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime
import logging

from odoo import _, api, fields, models
from odoo.tools import ormcache
from odoo.tools.safe_eval import safe_eval

try:
    from mailchimp3 import MailChimp
    from mailchimp3.mailchimpclient import MailChimpError
except ImportError:
    MailChimp = False
    MailChimpError = False


_logger = logging.getLogger(__name__)


class MailchimpList(models.Model):
    _name = "mailchimp.list"
    _description = "A mailchimp audience"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    mailchimp_id = fields.Char(required=True)
    interest_category_ids = fields.One2many(
        "mailchimp.interest.category", "list_id", string="Groups",
    )
    merge_field_ids = fields.One2many(
        "mailchimp.merge.field", "list_id", string="Merge fields",
    )
    group_ids = fields.Many2many("res.groups", help="Restricted to groups")

    @api.model
    @ormcache()
    def _get_mailchimp_client(self):
        return MailChimp(
            mc_api=self.env["ir.config_parameter"].get_param("crm_mailchimp.apikey"),
            mc_user=self.env["ir.config_parameter"].get_param("crm_mailchimp.username"),
        )

    @api.model
    def _read_from_mailchimp(self):
        client = self._get_mailchimp_client()
        for mailchimp_list in client.lists.all(
            get_all=True, fields="lists.name,lists.id"
        )["lists"]:
            this = self.search(
                [("mailchimp_id", "=", mailchimp_list["id"])]
            ) or self.create(
                {"name": mailchimp_list["name"], "mailchimp_id": mailchimp_list["id"]}
            )
            this._update_from_mailchimp()

    def _update_from_mailchimp(self):
        client = self._get_mailchimp_client()
        merge_field_model = self.env["mailchimp.merge.field"]
        interest_category_model = self.env["mailchimp.interest.category"]
        for this in self:
            # Update list itself.
            mailchimp_list = client.lists.get(this.mailchimp_id)
            this.write({"name": mailchimp_list["name"]})
            # Update merge fields.
            merge_field_model._update_from_mailchimp(client, this)
            # Update categories (including underlying interests).
            interest_category_model._update_from_mailchimp(client, this)

    def _push_to_mailchimp(self, modified_after=None):
        """Push partners to mailchimp."""
        date_domain = []
        if modified_after:
            date_domain = [("write_date", ">=", modified_after)]
        for this in self:
            for partner in self.env["res.partner"].search(
                date_domain
                + [("mailchimp_list_ids", "in", this.ids), ("email", "!=", False)]
            ):
                try:
                    this._push_partner_to_mailchimp(partner)
                except MailChimpError:
                    _logger.exception(
                        "Error pushing partner %d to mailchimp", partner,
                    )
            for partner in self.env["res.partner"].search(
                date_domain
                + [
                    ("mailchimp_deleted_list_ids", "in", this.ids),
                    ("email", "!=", False),
                ]
            ):
                try:
                    this._remove_partner_from_mailchimp(partner)
                except MailChimpError:
                    _logger.exception(
                        "Error pushing partner %d to mailchimp", partner,
                    )
                partner.write({"mailchimp_deleted_list_ids": [(3, this.id)]})

    def _remove_partner_from_mailchimp(self, partner):
        self.ensure_one()
        client = self._get_mailchimp_client()
        client.lists.members.delete(
            list_id=self.mailchimp_id, subscriber_hash=partner.mailchimp_id,
        )

    def _push_partner_to_mailchimp(self, partner):
        self.ensure_one()
        client = self._get_mailchimp_client()
        if partner.mailchimp_id:
            response = client.lists.members.create_or_update(
                list_id=self.mailchimp_id,
                subscriber_hash=partner.mailchimp_id,
                data=self._push_partner_to_mailchimp_data(partner),
            )
        else:
            response = client.lists.members.create(
                list_id=self.mailchimp_id,
                data=self._push_partner_to_mailchimp_data(partner),
            )
        if partner.mailchimp_id != response["id"]:
            _logger.debug(
                _("Partner %s has new mailchimp_id for email %s"),
                partner.display_name,
                partner.email,
            )
            partner.write({"mailchimp_id": response["id"]})

    def _push_partner_to_mailchimp_data(self, partner):
        """Get data from subscriber to push to Mailchimp, where code has been set."""
        self.ensure_one()
        merge_fields = {}
        for merge_field in self.merge_field_ids:
            if not merge_field.code:
                continue
            try:
                merge_fields[merge_field.tag] = safe_eval(
                    merge_field.code, {"partner": partner}, mode="eval"
                )
            except Exception:
                _logger.error(
                    _("Error getting data for merge-field %s, for partner %s"),
                    merge_field.tag,
                    partner.display_name,
                )
                raise
        interests = {
            interest.mailchimp_id: bool(partner.mailchimp_interest_ids & interest)
            for interest in self.mapped("interest_category_ids.interest_ids")
        }
        data = {
            "email_address": partner.email,
            "status": "subscribed",
            "status_if_new": "subscribed",
            "merge_fields": merge_fields,
            "interests": interests,
        }
        return data

    def action_update(self):
        return self._update_from_mailchimp()

    def action_push(self):
        return self._push_to_mailchimp()

    @api.model
    def _cron(self, lookbehind=None):
        modified_after = None
        if lookbehind:
            modified_after = fields.Datetime.to_string(
                datetime.datetime.now() - datetime.timedelta(seconds=lookbehind,)
            )
        self.search([])._push_to_mailchimp(modified_after=modified_after)
