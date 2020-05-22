# Copyright 2020 Adgensee - Vincent Garcies
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    taskcount = fields.Integer(
        string="Task", compute='_compute_task_count')

    def _compute_task_count(self):
        self.taskcount = len(self. task_ids)

    task_ids = fields.One2many("project.task", "lead_id", string="Tasks")
