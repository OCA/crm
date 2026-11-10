# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    lead_id = fields.Many2one("crm.lead")

    def action_view_lead(self):
        self.ensure_one()
        return self.lead_id._get_records_action(
            name=self.env._("Lead: %s", self.lead_id.name)
        )
