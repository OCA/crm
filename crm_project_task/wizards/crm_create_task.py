# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import _, fields, models
from odoo.exceptions import UserError


class CrmCreateTAsk(models.TransientModel):
    _name = "crm.create.task"
    _description = "Wizard to create task"

    task_name = fields.Char()
    description = fields.Html()

    def create_task(self):
        project = self.env.company.crm_default_project_id
        if not project:
            raise UserError(
                _(
                    "Project not configured in settings, "
                    "please contact with your administrator."
                )
            )
        lead = (
            self.env["crm.lead"].browse(self._context.get("active_id", False))
            if self._context.get("active_model") == "crm.lead"
            and self._context.get("active_id", False)
            else False
        )
        if not lead:
            raise UserError(
                _(
                    "Lead/Opportunity not found. Please, create task from lead/opportunity."
                )
            )

        # Create task
        task = (
            self.env["project.task"].sudo().create(self._get_data_create(lead, project))
        )
        # Messages in chatter
        task.message_post(
            body=_(
                "Task created from lead/opportunity "
                "<a href=# data-oe-model=crm.lead data-oe-id=%(lead)d>%(name)s</a>.",
                lead=lead,
                name=lead.name,
            )
        )
        lead.message_post(
            body=_(
                "Task <a href=# data-oe-model=project.task "
                "data-oe-id=%(task)d>%(name)s</a> created.",
                task=task,
                name=task.display_name,
            )
        )
        # Return action go to created task
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

    def _get_data_create(self, lead, project):
        """Get dict to create task"""
        return {
            "name": self.task_name,
            "project_id": project.id,
            "partner_id": lead.partner_id.id or False,
            "lead_id": lead.id,
            "description": self.description,
            "user_ids": [(6, 0, [])],
        }
