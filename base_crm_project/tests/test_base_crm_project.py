# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.mail.tests.common import mail_new_test_user


@tagged("post_install", "-at_install")
class TestBaseCrmProject(TransactionCase):
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
            }
        )
        cls.task = cls.env["project.task"].create(
            {"name": "Test Name", "lead_id": cls.lead.id}
        )

    def test_action_tasks(self):
        action = self.lead.action_tasks()
        tasks = self.env["project.task"].search(action["domain"])
        tasks_lead = tasks.mapped("lead_id")
        self.assertEqual(self.lead, tasks_lead)
