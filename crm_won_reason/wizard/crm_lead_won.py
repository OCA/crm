# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmLeadReason(models.TransientModel):
    _name = "crm.lead.won"
    _description = "Get Won Reason"

    won_reason_id = fields.Many2one(
        "crm.lost.reason",
        "Won Reason",
        domain="[('reason_type', 'in', (False, 'won'))]",
    )

    def action_win_reason_apply(self):
        leads = self.env["crm.lead"].browse(self.env.context.get("active_ids"))
        leads.action_set_won()
        return leads.write({"won_reason_id": self.won_reason_id.id})
