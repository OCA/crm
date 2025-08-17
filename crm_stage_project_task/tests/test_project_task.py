from .test_crm_stage_project_task_base import TestCrmStageProjectTaskCommon


class TestProjectTask(TestCrmStageProjectTaskCommon):
    def test_has_closed_states(self):
        # All state is not closed
        state = self.tasks._has_closed_states()
        self.assertFalse(state, "State must be False")

        # Task #1 -> Done
        self.task_1.state = "1_done"
        state = self.tasks._has_closed_states()
        self.assertFalse(state, "State must be False")

        # Task #1 -> Done, Task #2 -> Closed
        self.task_2.state = "1_canceled"
        state = self.tasks._has_closed_states()
        self.assertTrue(state, "State must be True")

    def test_attach_subtask_to_lead(self):
        self.task_1.update(
            {
                "lead_id": self.lead.id,
                "lead_stage_id": self.stage_team1_2.id,
            }
        )
        parent_vals = self.env["project.task"]._attach_subtask_to_lead(self.task_1.id)
        self.assertDictEqual(
            parent_vals,
            {
                "lead_id": self.lead.id,
                "lead_stage_id": self.stage_team1_2.id,
            },
        )

        empty_vals = self.env["project.task"]._attach_subtask_to_lead(False)
        self.assertEqual(empty_vals, {}, "Result must be empty dict")
