# Copyright 2010-2020 Odoo S. A.
# Copyright 2021 Tecnativa - Pedro M. Baeza
# Copyright 2022 Tecnativa - Víctor Martínez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import api, fields, models


class CrmLeadConvert2Task(models.TransientModel):
    """wizard to convert a Lead into a Project task
    and create a new task and link it to a lead"""

    _name = "crm.lead.convert2task"
    _description = "Lead convert or link to a Task"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        lead_id = self.env.context.get("active_id")
        if lead_id:
            result["lead_id"] = lead_id
        if self.env.context.get("default_project_id"):
            result["project_id"] = self.env.context["default_project_id"]
        return result

    lead_id = fields.Many2one(
        comodel_name="crm.lead", string="Lead", domain=[("type", "=", "lead")]
    )
    project_id = fields.Many2one(comodel_name="project.project", string="Project")

    def action_convert_lead_to_task(self):
        return self.lead_id._convert_lead_to_task(self.project_id)

    def action_link_task_to_lead(self):
        return self.lead_id._link_task_to_lead(self.project_id)
