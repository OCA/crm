# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestCrmStageAnalyticAccount(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.analytic_plan = cls.env["account.analytic.plan"].create(
            {"name": "Test Plan"}
        )
        cls.stage_new = cls.env["crm.stage"].create({"name": "New"})
        cls.stage_qualified = cls.env["crm.stage"].create(
            {
                "name": "Qualified",
                "create_analytic_account": True,
                "analytic_plan_id": cls.analytic_plan.id,
            }
        )
        cls.stage_qualified_no_plan = cls.env["crm.stage"].create(
            {
                "name": "Qualified No Plan",
                "create_analytic_account": True,
            }
        )

    def test_stage_without_flag_does_not_create_account(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": self.partner.id,
                "stage_id": self.stage_new.id,
            }
        )
        self.assertFalse(lead.analytic_account_id)

    def test_stage_with_flag_creates_account(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": self.partner.id,
                "stage_id": self.stage_new.id,
            }
        )
        lead.write({"stage_id": self.stage_qualified.id})
        self.assertTrue(lead.analytic_account_id)
        self.assertEqual(lead.analytic_account_id.name, lead.name)
        self.assertEqual(lead.analytic_account_id.partner_id, self.partner)
        self.assertEqual(lead.analytic_account_id.plan_id, self.analytic_plan)
        self.assertTrue(lead.analytic_account_id.code.startswith("FICHA/"))
        self.assertIn(
            lead.name,
            "".join(lead.analytic_account_id.message_ids.mapped("body")),
        )

    def test_stage_change_is_idempotent(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": self.partner.id,
                "stage_id": self.stage_qualified.id,
            }
        )
        account = lead.analytic_account_id
        self.assertTrue(account)
        lead.write({"stage_id": self.stage_new.id})
        lead.write({"stage_id": self.stage_qualified.id})
        self.assertEqual(lead.analytic_account_id, account)

    def test_stage_without_plan_does_not_create_account(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": self.partner.id,
                "stage_id": self.stage_new.id,
            }
        )
        lead.write({"stage_id": self.stage_qualified_no_plan.id})
        self.assertFalse(lead.analytic_account_id)
