# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def _compute_claim_count(self):
        claim_obj = self.env["crm.claim"]
        for analytic_account in self:
            domain = [("analytic_account_id", "=", analytic_account.id)]
            analytic_account.claim_count = claim_obj.search_count(domain)

    claim_count = fields.Integer(
        string="# Claims",
        compute="_compute_claim_count",
    )
