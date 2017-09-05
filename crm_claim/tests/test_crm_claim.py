# -*- coding: utf-8 -*-
# Copyright 2017 Vicent Cubells - <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestCrmClaim(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCrmClaim, cls).setUpClass()

        Claims = cls.env['crm.claim'].with_context(
            mail_create_nosubscribe=True)
        cls.claim = Claims.create({
            'name': 'Test Claim',
            'team_id': cls.env.ref('sales_team.team_sales_department').id,
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner Claim',
            'email': 'partner.claim@example.com',
            'phone': '1234567890',
        })

    def test_crm_claim(self):
        self.assertTrue(self.claim.stage_id.id)
        self.claim.partner_id = self.partner
        self.claim.onchange_partner_id()
        self.assertEqual(self.claim.email_from, self.partner.email)
        self.assertEqual(self.claim.partner_phone, self.partner.phone)
        self.assertEqual(self.partner.claim_count, 1)
        new_claim = self.claim.copy()
        self.assertEqual(new_claim.stage_id.id, 1)
        self.assertIn('copy', new_claim.name)
        self.assertTrue(new_claim.stage_id.id)
        self.assertEqual(self.partner.claim_count, 2)
