# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.tests.common import TransactionCase


class TestCrmLeadTask(TransactionCase):
    def setUp(self):
        super().setUp()

        # Create a CRM lead
        self.lead = self.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "description": "Description",
            }
        )

        # Create tasks related to the lead
        self.task1 = self.env["project.task"].create(
            {
                "name": "Test Task 1",
                "lead_id": self.lead.id,
            }
        )
        self.task2 = self.env["project.task"].create(
            {
                "name": "Test Task 2",
                "lead_id": self.lead.id,
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
        self.assertEqual(action["view_mode"], "tree,form")
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
