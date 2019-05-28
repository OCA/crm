# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError


class TestCrmStageMultiCompany(TransactionCase):
    def setUp(self):
        super(TestCrmStageMultiCompany, self).setUp()
        self.company = self.env["res.company"].create({"name": "Test Company"})
        self.stage_1 = self.env["crm.stage"].create(
            {"name": "Stage 1", "company_id": self.company.id}
        )
        self.stage_2 = self.env["crm.stage"].create(
            {"name": "Stage 2", "company_id": self.company.id}
        )
        self.stage_3 = self.env["crm.stage"].create(
            {"name": "Stage 3", "company_id": self.company.id}
        )
        self.user = self.env["res.users"].create(
            {
                "name": "test user",
                "login": "test",
                "company_id": self.company.id,
                "company_ids": (6, 0, [self.company.id]),
            }
        )

    def test_get_stages(self):
        stages = self.env["crm.stage"].sudo(self.user).search([])
        stages_2 = self.env["crm.stage"].search([("company_id","=", self.company.id)])
        self.assertEqual(set(stages), set(stages_2))

    def test_create_company_stage(self):
        with self.assertRaises(AccessError):
            self.env["crm.stage"].sudo(self.user).create(
                {"name": "Stage 4", "company_id": self.env.user.company_id.id}
            )

    def test_write_other_company_stage(self):
        with self.assertRaises(AccessError):
            self.env.ref("crm.stage_lead1").sudo(self.user).write({"name": "test"})

    def test_unlink_other_company_stage(self):
        with self.assertRaises(AccessError):
            self.env.ref("crm.stage_lead1").sudo(self.user).unlink()

