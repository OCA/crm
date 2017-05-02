# -*- coding: utf-8 -*-
# Copyright 2017 Vicent Cubells - <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


class TestCrmAction(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCrmAction, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
        })
        cls.pipeline = cls.env['crm.lead'].create({
            'name': 'Test lead',
            'partner_id': cls.partner.id,
        })
        cls.action1 = cls.env['crm.action'].create({
            'details': 'Test action #1',
        })
        cls.action2 = cls.env['crm.action'].create({
            'lead_id': cls.pipeline.id,
        })

    def test_crm_action(self):
        self.action1.lead_id = self.pipeline.id
        self.action1.check_change()
        self.assertEqual(self.action1.partner_id, self.partner)

        self.action1.button_confirm()
        self.assertEqual(self.action1.state, 'done')

        self.action1.button_set_to_draft()
        self.assertEqual(self.action1.state, 'draft')

        self.action1.button_confirm()

        self.assertEqual(self.action2.state, 'draft')
        self.assertEqual(
            self.pipeline.next_action_id, self.action2)

        self.action2.button_confirm()
        self.assertEqual(len(self.pipeline.next_action_id), 0)

        self.action2.button_set_to_draft()
        self.assertEqual(
            self.pipeline.next_action_id, self.action2)

        self.pipeline.next_action_done()
        self.assertEqual(
            self.action2.state, 'done')

        self.action2.button_set_to_draft()
        self.assertTrue(self.action2._send_email_reminder())

        self.action2.user_id.email = False
        self.action2._send_email_reminder()
