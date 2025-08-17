from datetime import timedelta

from freezegun import freeze_time
from markupsafe import Markup

from odoo import Command, fields
from odoo.exceptions import UserError

from .test_crm_stage_project_task_base import TestCrmStageProjectTaskCommon


class TestCrmTaskTemplate(TestCrmStageProjectTaskCommon):
    def test_check_delay(self):
        self.template_1.delay = 3
        self.assertEqual(self.template_1.delay, 3, "Delay must be equal to 3")

        with self.assertRaises(UserError):
            self.template_1.delay = -3

    @freeze_time("2025-11-01")
    def test_deadline(self):
        dt = self.template_1.deadline
        self.assertEqual(dt, fields.Datetime.now(), "Datetime's must be the same")

        self.template_1.delay = 1
        dt = self.template_1.deadline
        expect_dt = fields.Datetime.now() + timedelta(days=1)
        self.assertEqual(dt, expect_dt, "Datetime's must be the same")

    @freeze_time("2025-11-01")
    def test_prepare_project_task_vals(self):
        self.template_1.update({"delay_type": "hours", "delay": 3})
        project_task_vals_list = self.template_1._prepare_project_task_vals(self.lead)
        vals = project_task_vals_list[0]
        self.assertDictEqual(
            vals,
            {
                "name": "Template #1",
                "lead_id": self.lead.id,
                "project_id": self.project_pigs.id,
                "lead_stage_id": self.stage_team1_1.id,
                "description": Markup("<p>Test Template #1</p>"),
                "user_ids": [Command.set([])],
                "crm_task_template_id": self.template_1.id,
                "date_deadline": fields.Datetime.now() + timedelta(hours=3),
            },
        )

    @freeze_time("2025-11-01")
    def test_create_crm_tasks(self):
        self.template_1.update({"delay_type": "days", "delay": 5})

        task = self.template_1.create_crm_tasks(self.lead)

        self.assertTrue(task, "Task must be exists")

        self.assertRecordValues(
            task,
            [
                {
                    "name": "Template #1",
                    "lead_id": self.lead.id,
                    "project_id": self.project_pigs.id,
                    "lead_stage_id": self.stage_team1_1.id,
                    "description": Markup("<p>Test Template #1</p>"),
                    "crm_task_template_id": self.template_1.id,
                    "date_deadline": fields.Datetime.now() + timedelta(days=5),
                }
            ],
        )

        task = self.env["crm.task.template"].create_crm_tasks(self.lead)
        self.assertFalse(task, "Task must be empty")
