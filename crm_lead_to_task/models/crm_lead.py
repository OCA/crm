# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    task_ids = fields.One2many("project.task", "lead_id")
    task_count = fields.Integer(compute="_compute_task_count")
    crm_archive_lead_on_convert = fields.Boolean(
        related="company_id.crm_archive_lead_on_convert"
    )

    @api.depends("task_ids")
    def _compute_task_count(self):
        for lead in self:
            lead.task_count = len(lead.task_ids)

    def action_view_tasks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "list,form",
            "domain": [("lead_id", "=", self.id)],
            "context": {"default_search_lead_id": self.id},
            "name": _("Tasks from crm lead %s") % self.name,
        }

    def _get_values_task_from_lead(self, project):
        """Prepare values to create a task from the lead."""
        self.ensure_one()
        partner = self._find_matching_partner()
        if not partner and (self.partner_name or self.contact_name):
            self._handle_partner_assignment()
            partner = self.partner_id

        return {
            "name": self.name,
            "description": self.description,
            "project_id": project.id,
            "partner_id": partner.id,
            "email_cc": self.email_cc,
            "lead_id": self.id,
        }

    def _create_task_from_lead(self, project):
        vals = self._get_values_task_from_lead(project)
        task = self.env["project.task"].create(vals)

        # Move mail thread + attachments
        self.message_change_thread(task)

        self.env["ir.attachment"].search(
            [
                ("res_model", "=", "crm.lead"),
                ("res_id", "=", self.id),
            ]
        ).write({"res_model": "project.task", "res_id": task.id})

        return task

    def _action_create_and_open_task(self, project):
        task = self._create_task_from_lead(project)

        if self.company_id.crm_archive_lead_on_convert:
            self.active = False
        view = self.env.ref("project.view_task_form2")
        return {
            "name": "Task created",
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "form",
            "view_type": "form",
            "view_id": view.id,
            "res_id": task.id,
            "target": "current",
        }

    def action_crm_to_task(self):
        self.ensure_one()
        if self.company_id.crm_force_project_id:
            action = self._action_create_and_open_task(
                self.company_id.crm_force_project_id
            )
        else:
            action = self.env.ref(
                "crm_lead_to_task.crm_lead_convert2task_action"
            ).read()[0]
            action["context"] = {"default_lead_id": self.id}

        return action
