# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
    )
    analytic_amount = fields.Monetary(
        string="Amount",
        compute="_compute_analytic_amount",
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        readonly=True,
        store=True,
        compute_sudo=True,
    )

    def _compute_analytic_amount(self):
        line_obj = self.env["account.analytic.line"]
        for claim in self:
            lines = line_obj.search([("claim_id", "=", claim.id)])
            claim.analytic_amount = sum(lines.mapped("amount"))

    def button_account_analytic_line_action(self):
        self.ensure_one()
        action = self.env.ref("analytic.account_analytic_line_action_entries")
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
        action_dict["context"].update(
            {
                "search_default_claim_id": self.id,
                "default_claim_id": self.id,
                "default_account_id": self.analytic_account_id.id,
            }
        )
        domain = expression.AND(
            [
                [("account_id", "=", self.analytic_account_id.id)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict
