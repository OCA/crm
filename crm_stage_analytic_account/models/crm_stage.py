# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    create_analytic_account = fields.Boolean(
        help="If set, an analytic account will automatically be created "
        "and linked to the lead/opportunity when it reaches this stage.",
    )
    analytic_plan_id = fields.Many2one(
        comodel_name="account.analytic.plan",
        help="Analytic plan used to automatically create the analytic "
        "account when a lead/opportunity reaches this stage.",
    )
