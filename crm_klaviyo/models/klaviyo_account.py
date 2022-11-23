# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from klaviyo_api import KlaviyoAPI
from odoo import api, fields, models


class KlaviyoAccount(models.Model):
    _name = "klaviyo.account"
    _description = "API keys for Klaviyo"

    api_key = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company')

    @api.model
    def get_api(self, company=None):
        """Return an initialized API client for the current or given company"""
        if company is None:
            company = self.env.user._get_company()
        return self.sudo().search(
            [
                '|',
                ('company_id', '=', (company or self.env['res.company']).id),
                ('company_id', '=', False),
            ],
            limit=1, order='company_id asc',
        )._get_api()

    @api.multi
    def _get_api(self):
        """Return an initialized API client for the current record"""
        self.ensure_one()
        return KlaviyoAPI(self.api_key)
