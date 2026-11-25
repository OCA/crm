# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    lead_id = fields.Many2one("crm.lead")
    effective_lead_id = fields.Many2one(
        "crm.lead", compute="_compute_effective_lead_id"
    )

    def _compute_effective_lead_id(self):
        for task in self:
            lead = task.lead_id
            if not lead and task.parent_id:
                lead = task.parent_id.effective_lead_id
            task.effective_lead_id = lead

    def action_view_lead(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "crm.lead",
            "view_mode": "form",
            "res_id": self.lead_id.id,
            "target": "current",
            "name": self.env._("Lead: %s", self.lead_id.name),
        }
