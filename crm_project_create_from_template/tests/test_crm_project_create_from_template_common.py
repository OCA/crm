# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.mail.tests.common import mail_new_test_user


class TestCrmProjectCreateFromTemplateCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create({"name": "Company Test Template"})
        cls.user_salesman = mail_new_test_user(
            cls.env,
            login="user_template_salesman",
            name="User Template Salesman",
            email="user_template_salesman@test.example.com",
            company_id=cls.company.id,
            groups="sales_team.group_sale_salesman",
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner Test"})
        cls.template_partner = cls.env["res.partner"].create(
            {"name": "Template Partner Test"}
        )
        cls.project_template = cls.env["project.project"].create(
            {
                "name": "Template Project",
                "partner_id": cls.template_partner.id,
                "description": "<p>Template Description</p>",
                "company_id": cls.company.id,
                "allow_billable": False,
                "is_template": True,
            }
        )
        cls.regular_project = cls.env["project.project"].create(
            {
                "name": "Regular Project",
                "partner_id": cls.partner.id,
                "company_id": cls.company.id,
            }
        )
        cls.template_task = cls.env["project.task"].create(
            {
                "name": "Template Task",
                "project_id": cls.project_template.id,
                "description": "Template Task Description",
            }
        )

    def _create_lead(self, name):
        return self.env["crm.lead"].create(
            {
                "name": name,
                "type": "lead",
                "partner_id": self.partner.id,
                "user_id": self.user_salesman.id,
            }
        )

    def _create_wizard_form(self, lead):
        return Form(
            self.env["crm.create.project"].with_context(
                active_model="crm.lead",
                active_id=lead.id,
                default_lead_id=lead.id,
                default_project_name=lead.name,
            )
        )
