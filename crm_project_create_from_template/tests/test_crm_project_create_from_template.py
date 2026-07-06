# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from markupsafe import Markup

from odoo.tests.common import users

from .test_crm_project_create_from_template_common import (
    TestCrmProjectCreateFromTemplateCommon,
)


class TestCrmProjectCreateFromTemplate(TestCrmProjectCreateFromTemplateCommon):
    def test_project_template_domain(self):
        domain = self.env["crm.create.project"]._fields["project_template_id"].domain
        self.assertEqual(domain, [("is_template", "=", True)])
        self.assertTrue(self.project_template.is_template)
        self.assertFalse(self.regular_project.is_template)

    @users("user_template_salesman")
    def test_crm_create_project_without_template(self):
        lead = self._create_lead("Lead Without Template")
        wizard_form = self._create_wizard_form(lead)
        wizard_form.project_name = "Project Without Template"
        wizard_form.project_description = "Project Without Template Description"
        wizard = wizard_form.save()
        wizard.create_project()

        self.assertTrue(lead.project_id)
        self.assertEqual(lead.project_id.name, "Project Without Template")
        self.assertEqual(
            lead.project_id.description,
            Markup("<p>Project Without Template Description</p>"),
        )
        self.assertFalse(lead.project_id.task_ids)

    @users("user_template_salesman")
    def test_crm_create_project_from_template(self):
        lead = self._create_lead("Lead With Template")
        wizard_form = self._create_wizard_form(lead)
        wizard_form.project_template_id = self.project_template
        wizard_form.project_name = "Project From Template"
        wizard_form.project_description = "Project Description From Wizard"
        wizard = wizard_form.save()
        wizard.create_project()

        project = lead.project_id
        self.assertTrue(project)
        self.assertNotEqual(project, self.project_template)
        self.assertEqual(project.name, "Project From Template")
        self.assertEqual(project.partner_id, self.partner)
        self.assertEqual(project.company_id, self.company)
        self.assertEqual(
            project.description, Markup("<p>Project Description From Wizard</p>")
        )
        self.assertTrue(project.allow_billable)
        self.assertFalse(project.alias_name)
        self.assertEqual(project.task_ids.name, self.template_task.name)
        self.assertEqual(
            project.task_ids.description,
            Markup("<p>Template Task Description</p>"),
        )

    @users("user_template_salesman")
    def test_crm_create_project_from_template_preserve_description(self):
        lead = self._create_lead("Lead With Template Description")
        wizard_form = self._create_wizard_form(lead)
        wizard_form.project_template_id = self.project_template
        wizard_form.project_name = "Project From Template Description"
        wizard = wizard_form.save()
        wizard.create_project()

        self.assertEqual(
            lead.project_id.description,
            Markup("<p>Template Description</p>"),
        )
