# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _

from odoo.addons.base.tests.common import BaseCommon


class TestCrmLeadTask(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a CRM lead
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "description": "Description",
            }
        )

        # Create Project
        cls.project = cls.env["project.project"].create({"name": "Test Project"})

        # Create tasks related to the lead
        cls.task1 = cls.env["project.task"].create(
            {
                "name": "Test Task 1",
                "lead_id": cls.lead.id,
            }
        )
        cls.task2 = cls.env["project.task"].create(
            {
                "name": "Test Task 2",
                "lead_id": cls.lead.id,
            }
        )

    def test_task_count_computation(self):
        """Test that the task_count field correctly reflects the number of tasks"""
        lead = self.env["crm.lead"].browse(self.lead.id)
        self.assertEqual(lead.task_count, 2, "Task count should be 2.")

    def test_action_view_tasks(self):
        """Test that action_view_tasks returns the correct action"""
        action = self.lead.action_view_tasks()

        expected_domain = [("lead_id", "=", self.lead.id)]
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(action["view_mode"], "list,form")
        self.assertEqual(action["domain"], expected_domain)
        self.assertEqual(action["context"]["default_search_lead_id"], self.lead.id)
        self.assertEqual(action["name"], _("Tasks from crm lead %s") % self.lead.name)

    def test_action_view_leads(self):
        """Test that action_view_lead returns the correct action"""
        action = self.task1.action_view_lead()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "crm.lead")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["res_id"], self.lead.id)
        self.assertEqual(action["name"], _("Lead: %s") % self.lead.name)

    def test_create_task_from_lead(self):
        task = self.lead._create_task_from_lead(self.project)

        self.assertEqual(task.name, self.lead.name)
        self.assertEqual(task.description, self.lead.description)
        self.assertEqual(task.project_id, self.project)
        self.assertEqual(task.partner_id, self.lead.partner_id)
        self.assertEqual(task.lead_id, self.lead)
        self.assertIn(task, self.lead.task_ids)

    def test_action_create_and_open_task(self):
        action = self.lead._action_create_and_open_task(self.project)

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["view_type"], "form")
        self.assertTrue(action["res_id"])
        self.assertEqual(action["name"], "Task created")
        self.assertEqual(
            action["view_id"], self.lead.env.ref("project.view_task_form2").id
        )
