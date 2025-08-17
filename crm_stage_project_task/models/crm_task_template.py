from datetime import timedelta
from typing import Any

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


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
    delay_type = fields.Selection(
        [
            ("minutes", "Minutes"),
            ("hours", "Hours"),
            ("days", "Days"),
            ("weeks", "Weeks"),
        ],
        default="days",
        required=True,
    )
    delay = fields.Integer(
        default=0, help="If the value is 0, then the current date will be used."
    )
    has_default_project = fields.Boolean(related="stage_id.has_default_project")

    @api.constrains("delay")
    def _check_delay(self):
        for record in self:
            if record.delay < 0:
                raise UserError(_("The delay must be greater than or equal to 0!"))

    @property
    def deadline(self):
        self.ensure_one()
        now = fields.Datetime.now()
        if self.delay == 0:
            return now
        return now + timedelta(**{self.delay_type: self.delay})

    def _prepare_project_task_vals(self, lead) -> list[dict[str, Any]]:
        """
        Prepare vals list for create project task

        Args:
            lead (crm.lead) : crm lead record
        Returns:
            list: list of project task vals
        """
        project_id = self.env.company.stage_project_id.id
        return [
            {
                "name": record.name,
                "lead_id": lead.id,
                "project_id": project_id,
                "lead_stage_id": record.stage_id.id,
                "description": record.description,
                "user_ids": [Command.set(record.user_ids.ids)],
                "crm_task_template_id": record.id,
                "date_deadline": record.deadline,
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
