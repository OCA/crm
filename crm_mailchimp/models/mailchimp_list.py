# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime
import logging

from odoo import api, fields, models
from odoo.tools import ormcache

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
    model_ids = fields.One2many(
        comodel_name="mailchimp.list.model",
        inverse_name="list_id",
        string="Models that can have subscriptions for this list.",
    )
    interest_category_ids = fields.One2many(
        comodel_name="mailchimp.interest.category",
        inverse_name="list_id",
        string="Interests (Mailchimp groups)",
    )
    group_ids = fields.Many2many("res.groups", help="Restricted to groups")
    mailchimp_id = fields.Char(required=True)

    @api.model_create_multi
    def create(self, vals):
        """When an audience is created, automatically create appropiate models."""
        records = super().create(vals)
        models_model = self.env["mailchimp.list.model"]
        model_list = self._get_auto_create_models()
        for record in records:
            for model_name in model_list:
                models_model.create({"list_id": record.id, "model": model_name})
        return records

    def _get_auto_create_models(self):
        """Models that should automatically be created for each audience."""
        return ["res.partner"]

    @api.model
    @ormcache()
    def _get_mailchimp_client(self):
        """Activate the library to communicate with mailchimp."""
        config_model = self.env["ir.config_parameter"]
        return MailChimp(
            mc_api=config_model.sudo().get_param("crm_mailchimp.apikey"),
            mc_user=config_model.sudo().get_param("crm_mailchimp.username"),
        )

    @api.model
    def _read_from_mailchimp(self):
        """Used from settings to get all audiences."""
        client = self._get_mailchimp_client()
        for mailchimp_list in client.lists.all(
            get_all=True, fields="lists.name,lists.id"
        )["lists"]:
            audience = self.search([("mailchimp_id", "=", mailchimp_list["id"])])
            if not audience:
                audience = self.create(
                    {
                        "name": mailchimp_list["name"],
                        "mailchimp_id": mailchimp_list["id"],
                    }
                )
            audience._update_from_mailchimp()

    def _update_from_mailchimp(self):
        client = self._get_mailchimp_client()
        merge_field_model = self.env["mailchimp.merge.field"]
        interest_category_model = self.env["mailchimp.interest.category"]
        for this in self:
            # Update list itself.
            mailchimp_list = client.lists.get(this.mailchimp_id)
            this.write({"name": mailchimp_list["name"]})
            # Update categories (including underlying interests).
            interest_category_model._update_from_mailchimp(client, this)
            # Update merge fields.
            for mailchimp_model in this.model_ids:
                merge_field_model._update_from_mailchimp(client, mailchimp_model)

    def _push_to_mailchimp(self, modified_after=None):
        """Push aubscriber to mailchimp."""
        client = self._get_mailchimp_client()
        for mailchimp_model in self.mailchimp_model_ids:
            mailchimp_model._push_to_mailchimp(client)

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
