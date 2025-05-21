# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    claim_id = fields.Many2one(
        comodel_name="crm.claim",
        domain='[("analytic_account_id", "=", account_id)]',
    )
