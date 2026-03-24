# Copyright 2023 Moduon Team S.L.
# Copyright 2026 Liam Noonan
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Domain


class CrmLead(models.Model):
    _inherit = "crm.lead"

    task_ids = fields.One2many("project.task", "lead_id")
    task_count = fields.Integer(
        "#Task", compute_sudo=True, compute="_compute_task_count"
    )

    @api.depends("task_ids")
    def _compute_task_count(self):
        for lead in self:
            lead.task_count = len(lead.task_ids)

    def _get_crm_default_project(self):
        self.ensure_one()
        return (
            self.company_id.crm_default_project_id
            or self.env.company.crm_default_project_id
        )

    def _can_create_task_natively(self, project=None):
        self.ensure_one()
        project = project or self._get_crm_default_project()
        return bool(
            project
            and self.env.user.has_group("project.group_project_user")
            and project.has_access("read")
        )

    def action_create_task(self):
        self.ensure_one()
        project = self._get_crm_default_project()
        if not project:
            raise UserError(
                self.env._(
                    "Project not configured in settings. "
                    "Please contact your administrator."
                )
            )
        if self._can_create_task_natively(project):
            action = self.env["ir.actions.actions"]._for_xml_id(
                "crm_project_task.action_new_task"
            )
        else:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "crm_project_task.wizard_crm_create_task_action"
            )
        action["context"] = self._get_default_context()
        return action

    def action_view_tasks(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "crm_project_task.action_crm_lead_related_tasks"
        )
        ctx = self._get_default_context()
        if not self._can_create_task_natively():
            ctx["create"] = False
        action["context"] = {
            "search_default_open_tasks": 1,
            **ctx,
        }
        action["domain"] = Domain.AND(
            [[("lead_id", "=", self.id)], self._get_lead_task_domain()]
        )
        return action

    def _get_default_context(self):
        """Get dict to create task context"""
        self.ensure_one()
        project = self._get_crm_default_project()
        return {
            "default_name": self.name,
            "default_project_id": project.id,
            "default_partner_id": self.partner_id.id,
            "default_lead_id": self.id,
            "default_user_ids": [fields.Command.set(self.user_id.ids)],
        }

    def _get_lead_task_domain(self):
        return []

    def _merge_get_fields_specific(self):
        fields_info = super()._merge_get_fields_specific()
        # If a res.company.crm_default_project_id in Company1 is set to a project in
        # Company2, this sudo prevents a user with access only to Company1 from
        # merging leads that have linked tasks in Company2. He will get an access error
        # if he tries. Not including the sudo would result in the tasks on the merged
        # lead to simply loose their connection to the merge target lead, which would
        # be worse.
        fields_info["task_ids"] = lambda fname, leads: [
            (4, task.id) for task in leads.sudo().mapped("task_ids")
        ]
        return fields_info
