# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmCreateProject(models.TransientModel):
    _inherit = "crm.create.project"

    project_template_id = fields.Many2one(
        comodel_name="project.project",
        string="Project Template",
        domain=[("is_template", "=", True)],
        help="Project to copy when creating the new project.",
    )

    def create_project(self):
        self.ensure_one()
        if not self.project_template_id:
            return super().create_project()
        project = self.project_template_id.sudo().copy(
            default=self._prepare_create_project_from_template_values()
        )
        self._link_project_to_lead(project)
        return None

    def _prepare_create_project_from_template_values(self):
        values = self._prepare_create_project_values()
        values["alias_name"] = False
        if not self.project_description:
            values.pop("description", None)
        return values

    def _link_project_to_lead(self, project):
        self.lead_id.project_id = project
        project.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": self.lead_id.project_id, "origin": self.lead_id},
            subtype_id=self.env.ref("mail.mt_note").id,
            author_id=self.env.user.partner_id.id,
        )
        self.lead_id.message_post_with_source(
            "mail_message_destiny_link_template.message_destiny_link",
            render_values={"self": self.lead_id, "destiny": self.lead_id.project_id},
            subtype_id=self.env.ref("mail.mt_note").id,
            author_id=self.env.user.partner_id.id,
        )
