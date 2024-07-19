# Copyright 2010-2020 Odoo S. A.
# Copyright 2021 Tecnativa - Pedro M. Baeza
# Copyright 2022 Tecnativa - Víctor Martínez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import api, fields, models


class CrmLeadConvert2Task(models.TransientModel):
    """wizard to convert a Lead into a Project task and move the Mail Thread"""

    _name = "crm.lead.convert2task"
    _description = "Lead convert to Task"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        lead_id = self.env.context.get("active_id")
        if lead_id:
            result["lead_id"] = lead_id
        return result

    lead_id = fields.Many2one(
        comodel_name="crm.lead", string="Lead", domain=[("type", "=", "lead")]
    )
    project_id = fields.Many2one(comodel_name="project.project", string="Project")

    def action_lead_to_project_task(self):
        self.ensure_one()
        # get the lead to transform
        lead = self.lead_id
        partner = lead._find_matching_partner()
        if not partner and (lead.partner_name or lead.contact_name):
            lead._handle_partner_assignment()
            partner = lead.partner_id
        # create new project.task
        vals = {
            "name": lead.name,
            "description": lead.description,
            "project_id": self.project_id.id,
            "partner_id": partner.id,
            "email_cc": lead.email_cc,
        }
        task = self.env["project.task"].create(vals)
        # move the mail thread
        lead.message_change_thread(task)
        # move attachments
        attachments = self.env["ir.attachment"].search(
            [("res_model", "=", "crm.lead"), ("res_id", "=", lead.id)]
        )
        attachments.write({"res_model": "project.task", "res_id": task.id})
        # archive the lead (can't be unlinked by plain salesmen)
        lead.active = False
        # return the action to go to the form view of the new Task
        view = self.env.ref("project.view_task_form2")
        return {
            "name": "Task created",
            "view_type": "form",
            "view_mode": "form",
            "view_id": view.id,
            "res_model": "project.task",
            "type": "ir.actions.act_window",
            "res_id": task.id,
            "context": self.env.context,
        }
