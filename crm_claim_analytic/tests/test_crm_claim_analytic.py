# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestCrmClaimAnalytic(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.analytic_plan = cls.env["account.analytic.plan"].create(
            {
                "name": "Test Analytic Plan",
            }
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Test Analytic Account",
                "plan_id": cls.analytic_plan.id,
            }
        )
        cls.claim = cls.env["crm.claim"].create(
            {
                "name": "Test Claim",
                "analytic_account_id": cls.analytic_account.id,
            }
        )
        cls.analytic_obj = cls.env["account.analytic.line"]

    def test_crm_claim_analytic(self):
        self.assertEqual(self.analytic_account.claim_count, 1)
        self.analytic_obj.create(
            {
                "name": "Test Line 1",
                "account_id": self.analytic_account.id,
                "amount": 100.0,
            }
        )
        self.analytic_obj.create(
            {
                "name": "Test Line 2",
                "account_id": self.analytic_account.id,
                "claim_id": self.claim.id,
                "amount": 50.0,
            }
        )
        self.assertEqual(self.claim.analytic_amount, 50.0)
        action_dict = self.claim.button_account_analytic_line_action()
        self.assertTrue("search_default_claim_id" in action_dict["context"])
        self.assertEqual(
            self.claim.id, action_dict["context"].get("search_default_claim_id")
        )
        self.assertIn(
            ("account_id", "=", self.claim.analytic_account_id.id),
            action_dict["domain"],
        )
