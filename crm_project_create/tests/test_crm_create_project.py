# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from markupsafe import Markup

from odoo.tests import Form
from odoo.tests.common import TransactionCase, users

from odoo.addons.mail.tests.common import mail_new_test_user


class TestCrmCreateProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create(
            {
                "name": "Company Test",
            }
        )
        cls.user_salesman = mail_new_test_user(
            cls.env,
            login="user_salesman",
            name="User Salesman",
            email="user_salesman@test.example.com",
            company_id=cls.company.id,
            groups="sales_team.group_sale_salesman",
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner Test",
            }
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "lead",
                "partner_id": cls.partner.id,
                "user_id": cls.user_salesman.id,
            }
        )

    @users("user_salesman")
    def test_crm_create_project(self):
        """Test the creation of a project from a lead."""
        wizard_form = Form(
            self.env["crm.create.project"].with_context(
                active_model="crm.lead",
                active_id=self.lead.id,
                default_lead_id=self.lead.id,
                default_project_name=self.lead.name,
            )
        )
        self.assertEqual(wizard_form.project_name, self.lead.name)

        wizard_form.project_name = "Test Project"
        wizard_form.project_description = "Test Description"
        wizard = wizard_form.save()
        wizard.create_project()

        self.assertTrue(self.lead.project_id)
        self.assertEqual(self.lead.project_id.name, "Test Project")
        self.assertEqual(
            self.lead.project_id.description,
            Markup("<p>Test Description</p>"),
        )
