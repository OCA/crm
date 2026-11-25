# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        copy=False,
        readonly=True,
        tracking=True,
        help="Analytic account automatically created when this lead/"
        "opportunity reached a stage configured to create one.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)
        leads._create_analytic_account_from_stage()
        return leads

    def write(self, vals):
        res = super().write(vals)
        if "stage_id" in vals:
            self._create_analytic_account_from_stage()
        return res

    def _create_analytic_account_from_stage(self):
        for lead in self:
            if (
                lead.stage_id.create_analytic_account
                and lead.stage_id.analytic_plan_id
                and not lead.analytic_account_id
            ):
                lead._create_analytic_account()

    def _create_analytic_account(self):
        self.ensure_one()
        analytic_account = (
            self.env["account.analytic.account"]
            .sudo()
            .create(self._prepare_analytic_account_values())
        )
        self.analytic_account_id = analytic_account
        analytic_account.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": analytic_account, "origin": self},
            subtype_id=self.env.ref("mail.mt_note").id,
            author_id=self.env.user.partner_id.id,
        )

    def _prepare_analytic_account_values(self):
        self.ensure_one()
        return {
            "name": self.name,
            "code": self.env["ir.sequence"].next_by_code("crm.lead.analytic.account"),
            "partner_id": self.partner_id.id,
            "company_id": self.company_id.id,
            "plan_id": self.stage_id.analytic_plan_id.id,
        }
