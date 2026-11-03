# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    lead_id = fields.Many2one("crm.lead")

    def action_open_parent_lead(self):
        return {
            "name": self.env._("Parent Lead"),
            "view_mode": "form",
            "res_model": "crm.lead",
            "res_id": self.lead_id.id,
            "type": "ir.actions.act_window",
            "context": self.env.context,
        }
