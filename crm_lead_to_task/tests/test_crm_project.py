# Copyright 2021 Tecnativa - Pedro M. Baeza
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo.tests import common


class TestCrmProject(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test lead",
                "description": "Description",
                "email_from": "test@example.org",
                "partner_name": "Test partner",
            }
        )
        cls.project = cls.env["project.project"].create({"name": "Test project"})

    def test_crm_project(self):
        wizard = (
            self.env["crm.lead.convert2task"]
            .with_context(active_id=self.lead.id,)
            .create({"project_id": self.project.id})
        )
        action = wizard.action_lead_to_project_task()
        task = self.env["project.task"].browse(action["res_id"])
        self.assertEqual(task.description, "<p>Description</p>")
        self.assertEqual(task.email_from, "test@example.org")
        self.assertEqual(task.partner_id.name, "Test partner")
        self.assertEqual(task.project_id, self.project)
        self.assertFalse(self.lead.exists())
