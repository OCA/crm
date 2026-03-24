# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models
from odoo.exceptions import UserError


class CrmCreateTAsk(models.TransientModel):
    _name = "crm.create.task"
    _description = "Wizard to create task"

    lead_id = fields.Many2one("crm.lead")
    task_name = fields.Char()
    description = fields.Html()

    def create_task(self):
        project = self.lead_id._get_crm_default_project()
        if not project:
            raise UserError(
                self.env._(
                    "Project not configured in settings. "
                    "Please contact your administrator."
                )
            )
        task = self.env["project.task"].sudo().create(self._get_data_create(project))
        # Creator is automatically subscribed to the task, giving him access to it even
        # though he has no access on the project. We prevent this by unsubscribing him.
        creator = self.env.user.partner_id
        if creator in task.message_partner_ids:
            task.message_unsubscribe(partner_ids=creator.ids)

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
