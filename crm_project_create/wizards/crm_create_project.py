# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmCreateProject(models.TransientModel):
    _name = "crm.create.project"
    _description = "Wizart to create Project from Lead/Opportunity"

    project_name = fields.Char()
    project_description = fields.Html()
    lead_id = fields.Many2one("crm.lead")

    def create_project(self):
        project = (
            self.env["project.project"]
            .sudo()
            .create(self._prepare_create_project_values())
        )
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

    def _prepare_create_project_values(self):
        return {
            "name": self.project_name,
            "partner_id": self.lead_id.partner_id.id,
            "description": self.project_description,
            "active": True,
            "company_id": self.lead_id.company_id.id,
            "allow_billable": True,
        }
