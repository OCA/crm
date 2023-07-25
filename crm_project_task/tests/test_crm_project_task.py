# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.mail.tests.common import mail_new_test_user


@tagged("post_install", "-at_install")
class TestCrmProjectTask(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.user.company_id
        cls.user_salesman = mail_new_test_user(
            cls.env,
            login="user_test",
            name="User Test",
            email="user_test@test.example.com",
            company_id=cls.company.id,
            groups="sales_team.group_sale_salesman",
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner Test",
            }
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "lead",
                "partner_id": cls.partner.id,
                "user_id": cls.user_salesman.id,
            }
        )
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
                "description": "Test Description",
            }
        )

    def test_create_task(self):
        self.company.crm_default_project_id = self.project
        task_name = "Task Test"
        task_description = "Line1</br>Line2"
        action = (
            self.env["crm.create.task"]
            .with_user(self.user_salesman)
            .create(
                {
                    "lead_id": self.lead.id,
                    "task_name": task_name,
                    "description": task_description,
                }
            )
            .create_task()
        )
        task = self.env["project.task"].browse(action["res_id"])
        self.assertEqual(task.name, task_name)
        self.assertEqual(task.project_id, self.company.crm_default_project_id)
        self.assertEqual(task.partner_id, self.partner)
        self.assertEqual(task.lead_id, self.lead)

    def test_create_task_no_project(self):
        self.company.crm_default_project_id = False
        task_name = "Task Test"
        task_description = "Line1</br>Line2"
        wizard = (
            self.env["crm.create.task"]
            .with_user(self.user_salesman)
            .create(
                {
                    "lead_id": self.lead.id,
                    "task_name": task_name,
                    "description": task_description,
                }
            )
        )
        with self.assertRaises(UserError):
            wizard.create_task()

    def test_action_tasks(self):
        self.company.crm_default_project_id = self.project
        self.env["crm.create.task"].with_user(self.user_salesman).create(
            {
                "lead_id": self.lead.id,
                "task_name": "Task Test",
                "description": "Line1</br>Line2",
            }
        ).create_task()
        action = self.lead.action_tasks()
        tasks = self.env["project.task"].search(action["domain"])
        tasks_lead = tasks.mapped("lead_id")
        self.assertEqual(self.lead, tasks_lead)
