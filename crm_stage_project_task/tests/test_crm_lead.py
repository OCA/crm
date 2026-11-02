from odoo.exceptions import UserError

from .test_crm_stage_project_task_base import TestCrmStageProjectTaskCommon


class TestCrmLeadFlow(TestCrmStageProjectTaskCommon):
    def test_can_change_stage(self):
        """
        Test flow where check the possibility
        to change stage for crm lead.
        """
        # Create a new lead

        self.assertFalse(self.lead.task_ids, "Lead tasks must be empty")

        self.lead.stage_id = self.stage_team1_2

        # Lead with unclosed tasks
        result = self.lead._can_change_stage()
        self.assertFalse(result, "Result must be False")

        # Disable check task state for crm lead
        self.stage_team1_2.check_task_state = False
        result = self.lead._can_change_stage()
        self.assertTrue(result, "Result must be True")

        # Set "Done" for all crm tasks
        self.stage_team1_2.check_task_state = True
        self.lead.task_ids.write({"state": "1_done"})
        result = self.lead._can_change_stage()
        self.assertTrue(result, "Result must be True")

        # Empty crm lead record
        result = self.env["crm.lead"]._can_change_stage()
        self.assertTrue(result, "Result must be True")

    def test_create_task_by_template01(self):
        self.lead.stage_id = self.stage_team1_2
        self.assertRecordValues(
            self.lead.task_ids,
            [
                {"name": "Test Task #1", "project_id": self.project_pigs.id},
                {"name": "Test Task #2", "project_id": self.project_pigs.id},
            ],
        )

    def test_create_tasks_by_template02(self):
        self.env.company.stage_project_id = False
        self.lead.stage_id = self.stage_team1_2
        self.assertRecordValues(
            self.lead.task_ids,
            [
                {"name": "Test Task #1", "project_id": False},
                {"name": "Test Task #2", "project_id": False},
            ],
        )

    def test_crm_lead_flow(self):
        self.lead.stage_id = self.stage_team1_2
        self.assertRecordValues(
            self.lead.task_ids,
            [
                {"name": "Test Task #1", "project_id": self.project_pigs.id},
                {"name": "Test Task #2", "project_id": self.project_pigs.id},
            ],
        )
        with self.assertRaises(UserError):
            self.lead.stage_id = self.stage_team1_won
        self.lead.task_ids.write({"state": "1_done"})
        self.lead.stage_id = self.stage_team1_won
        self.assertEqual(
            self.lead.stage_id, self.stage_team1_won, "Stages must be the same"
        )
