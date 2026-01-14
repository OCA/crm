# Copyright 2026 Binhex - Adasat Torres de León
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    capital_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Capital country",
        help="Country of origin of this company's capital.",
    )
    capital_amount = fields.Monetary(
        string="Capital amount",
        currency_field="capital_currency_id",
        help="Publicly registered capital amount.",
    )
    capital_currency_id = fields.Many2one(
        comodel_name="res.currency", string="Capital currency"
    )
    turnover_range_id = fields.Many2one(
        comodel_name="res.partner.turnover_range", string="Turnover range"
    )
    turnover_amount = fields.Float()
    company_size = fields.Selection(
        string="Company size",
        selection=[
            ("micro", "Micro"),
            ("small", "Small"),
            ("medium", "Medium"),
            ("big", "Big"),
        ],
    )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(partner_name, is_company, parent_id)
        if is_company:
            res.update(
                {
                    "capital_country_id": self.capital_country_id.id,
                    "capital_amount": self.capital_amount,
                    "capital_currency_id": self.capital_currency_id.id,
                    "turnover_range_id": self.turnover_range_id.id,
                    "turnover_amount": self.turnover_amount,
                    "company_size": self.company_size,
                }
            )
        return res
