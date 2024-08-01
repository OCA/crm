# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    task_ids = fields.One2many('project.task', 'lead_id')
    task_count = fields.Integer(compute="_compute_task_count")

    @api.depends('task_ids')
    def _compute_task_count(self):
        for lead in self:
            lead.task_count = len(lead.task_ids)

    def action_view_tasks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "tree,form",
            "domain": [('lead_id', '=', self.id)],
            "context": {"default_search_lead_id": self.id},
            "name": _("Tasks from crm lead %s") % self.name,
        }
