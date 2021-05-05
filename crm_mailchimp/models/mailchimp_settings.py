# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import hashlib

from odoo import api, fields, models


class MailchimpSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _name = "mailchimp.settings"
    _description = "Mailchimp settings"

    username = fields.Char(required=True, config_parameter="crm_mailchimp.username")
    apikey = fields.Char(required=True, config_parameter="crm_mailchimp.apikey")

    def execute(self):
        result = super(MailchimpSettings, self).execute()
        if result:
            self.env["mailchimp.list"]._read_from_mailchimp()
        return result

    @api.model
    def _get_webhook_key(self):
        return hashlib.sha1(
            self.env["ir.config_parameter"].get_param("database.secret")
            + self.env["ir.config_parameter"].get_param("web.base.url")
        ).hexdigest()
