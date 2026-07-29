from odoo import Command

from odoo.addons.crm.tests.common import TestCrmCommon
from odoo.addons.project.tests.test_project_base import TestProjectCommon


class TestCrmStageProjectTaskCommon(TestCrmCommon, TestProjectCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.env.company.stage_project_id = cls.project_pigs

        cls.stage_team1_2.write(
            {
                "check_task_state": True,
                "task_template_ids": [
                    Command.create({"name": "Test Task #1"}),
                    Command.create({"name": "Test Task #2"}),
                ],
            }
        )

    def setUp(self):
        super().setUp()
        self.lead = self.env["crm.lead"].create(
            {"name": "Lead With Tasks", "stage_id": self.stage_team1_1.id}
        )
        self.task_1, self.task_2 = self.env["project.task"].create(
            [
                {"name": "Task #1"},
                {"name": "Task #2"},
            ]
        )
        self.tasks = self.task_1 | self.task_2

        self.template_1 = self.env["crm.task.template"].create(
            {
                "name": "Template #1",
                "stage_id": self.stage_team1_1.id,
                "description": "Test Template #1",
            }
        )
