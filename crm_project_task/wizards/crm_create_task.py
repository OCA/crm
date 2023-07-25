# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import _, fields, models
from odoo.exceptions import UserError


class CrmCreateTAsk(models.TransientModel):
    _name = "crm.create.task"
    _description = "Wizard to create task"

    lead_id = fields.Many2one("crm.lead")
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
        # Create task
        task = self.env["project.task"].sudo().create(self._get_data_create(project))
        # Messages in chatter
        task.message_post(
            body=_(
                "Task created from lead/opportunity "
                "<a href=# data-oe-model=crm.lead data-oe-id=%(lead)d>%(name)s</a>.",
                lead=self.lead_id,
                name=self.lead_id.name,
            )
        )
        self.lead_id.message_post(
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

    def _get_data_create(self, project):
        """Get dict to create task"""
        return {
            "name": self.task_name,
            "project_id": project.id,
            "partner_id": self.lead_id.partner_id.id,
            "lead_id": self.lead_id.id,
            "description": self.description,
            "user_ids": [(6, 0, [])],
        }
