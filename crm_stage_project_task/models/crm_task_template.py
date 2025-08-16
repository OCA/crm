from odoo import Command, fields, models


class CrmTaskTemplate(models.Model):
    _name = "crm.task.template"
    _description = "CRM Task Template"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    stage_id = fields.Many2one("crm.stage", required=True, ondelete="cascade")
    description = fields.Html()
    user_ids = fields.Many2many(
        "res.users",
        string="Assigned",
        default=lambda self: self.env.user,
        help="Assigned user by default",
    )
    task_ids = fields.One2many(
        "project.task",
        "crm_task_template_id",
    )

    def _prepare_project_task_vals(self, lead) -> list[dict]:
        """
        Prepare vals list for create project task

        Args:
            lead (crm.lead) : crm lead record
        Returns:
            list: list of project task vals
        """
        company_id = self.env.company.stage_project_id.id
        return [
            {
                "name": "name",
                "lead_id": lead.id,
                "project_id": company_id,
                "lead_stage_id": record.stage_id.id,
                "description": "description",
                "user_ids": [Command.set(record.user_ids.ids)],
                "crm_task_template_id": record.id,
            }
            for record in self
        ]

    def create_crm_tasks(self, lead):
        """
        Create project task for crm lead by crm task template

        Args:
            lead (crm.lead): crm lead record
        Returns:

        """
        task_vals_list = self._prepare_project_task_vals(lead)
        if not task_vals_list:
            return self.env["project.task"]
        return self.env["project.task"].sudo().create(task_vals_list)
