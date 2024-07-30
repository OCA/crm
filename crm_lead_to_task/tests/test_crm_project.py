# Copyright 2021 Tecnativa - Pedro M. Baeza
# Copyright 2022 Tecnativa - Víctor Martínez
# Copyright 2024 Tecnativa - Carolina Fernandez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo.addons.base.tests.common import BaseCommon


class TestCrmProject(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test lead",
                "description": "Description",
                "partner_name": "Test partner crm_lead_to_task",
                "email_cc": "cc@example.org",
            }
        )
        cls.project = cls.env["project.project"].create({"name": "Test project"})

    def test_crm_project(self):
        wizard = (
            self.env["crm.lead.convert2task"]
            .with_context(
                active_id=self.lead.id,
            )
            .create({"project_id": self.project.id})
        )
        action = wizard.action_lead_to_project_task()
        task = self.env["project.task"].browse(action["res_id"])
        self.assertEqual(task.description, "<p>Description</p>")
        self.assertEqual(task.email_cc, "cc@example.org")
        self.assertEqual(task.partner_id.name, "Test partner crm_lead_to_task")
        self.assertEqual(task.project_id, self.project)
        self.assertFalse(self.lead.active)
