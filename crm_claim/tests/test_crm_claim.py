# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestCrmClaim(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.claim = cls.env["crm.claim"].create(
            {
                "name": "Test Claim",
                "team_id": cls.env.ref("sales_team.salesteam_website_sales").id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner Claim",
                "email": "partner.claim@example.com",
                "phone": "1234567890",
            }
        )
        cls.claim_categ = cls.env.ref("crm_claim.categ_claim1")
        cls.sales_team = cls.claim_categ.team_id

    def test_crm_claim_misc(self):
        self.assertNotEqual(self.claim.team_id, self.sales_team)
        self.assertTrue(self.claim.stage_id)
        claim_form = Form(self.claim)
        claim_form.partner_id = self.partner
        self.assertEqual(claim_form.email_from, self.partner.email)
        self.assertEqual(claim_form.partner_phone, self.partner.phone)
        claim_form.categ_id = self.claim_categ
        self.assertEqual(claim_form.team_id, self.sales_team)
        self.claim = claim_form.save()
        self.assertEqual(self.partner.claim_count, 1)
        new_claim = self.claim.copy()
        self.assertEqual(new_claim.stage_id.id, self.claim._get_default_stage_id())
        self.assertIn("copy", new_claim.name)
        self.assertTrue(new_claim.stage_id)
        self.assertEqual(self.partner.claim_count, 2)

    def test_crm_claim_report(self):
        items = self.env["crm.claim.report"].search(
            [("team_id", "=", self.claim.team_id.id)]
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items.id, self.claim.id)
