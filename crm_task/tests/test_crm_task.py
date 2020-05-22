# Copyright 2020 Adgensee - Vincent Garcies
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestCrmTask(common.TransactionCase):

    def test_create_data(self):
        # Create a new lead with the test
        test_crm_lead = self.env['crm.lead'].create({
            'name': 'TestLead'
        })

        # Add a test task to the lead
        test_project_task = self.env['project.task'].create({
            'name': 'ExampleTask',
            'lead_id': test_crm_lead.id
        })

        # Check if the lead name and the task name match
        self.assertEqual(test_crm_lead.name, 'TestLead')
        self.assertEqual(test_project_task.name, 'ExampleTask')
        # Check if the task assigned to the lead is in fact the correct id
        self.assertEqual(test_project_task.lead_id.id, test_crm_lead.id)
