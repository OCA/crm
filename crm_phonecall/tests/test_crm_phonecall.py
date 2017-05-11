# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestCrmPhoneCall(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCrmPhoneCall, cls).setUpClass()
        cls.company = cls.env.ref('base.main_company')
        partner_obj = cls.env['res.partner']
        cls.partner1 = partner_obj.create({
            'name': 'Partner1',
            'phone': '123 456 789',
            'mobile': '123 456 789',
            'type': 'contact',
        })
        cls.partner2 = partner_obj.create({
            'name': 'Partner2',
            'phone': '789 654 321',
            'mobile': '789 654 321',
        })
        cls.phonecall1 = cls.env['crm.phonecall'].create({
            'name': 'Call #1 for test',
            'partner_id': cls.partner1.id,
        })
        cls.opportunity1 = cls.env['crm.lead'].create({
            'name': 'Opportunity #1',
            'phone': '12345',
            'mobile': '6789',
            'partner_id': cls.partner1.id,
        })
        cls.opportunity2 = cls.env['crm.lead'].create({
            'name': 'Opportunity #2',
            'phone': '2222',
            'mobile': '3333',
            'partner_id': cls.partner2.id,
        })
        cls.tag = cls.env.ref('crm.categ_oppor1')

    def test_on_change_partner(self):
        self.phonecall1.partner_id = self.partner2
        self.phonecall1.on_change_partner_id()
        self.assertEqual(self.phonecall1.partner_phone, self.partner2.phone)
        self.assertEqual(self.phonecall1.partner_mobile, self.partner2.mobile)

        self.assertFalse(self.phonecall1.date_closed)
        self.phonecall1.state = 'done'
        self.assertTrue(self.phonecall1.date_closed)
        self.phonecall1.state = 'open'
        self.assertEqual(self.phonecall1.duration, 0.0)

    def test_schedule_another_phonecall(self):
        self.phonecall2 = self.phonecall1.schedule_another_phonecall(
            schedule_time=False,
            call_summary='Test schedule method',
            action='schedule',
            tag_ids=self.tag.id,
        )[self.phonecall1.id]
        self.assertEqual(self.phonecall2.id, self.phonecall1.id + 1)
        self.assertEqual(self.phonecall1.state, 'open')
        self.phonecall3 = self.phonecall1.schedule_another_phonecall(
            schedule_time='2017-12-31 00:00:00',
            call_summary='Test schedule method2',
            action='log',
        )[self.phonecall1.id]
        self.assertEqual(self.phonecall3.id, self.phonecall1.id + 2)
        self.assertEqual(self.phonecall1.state, 'done')

        result = self.phonecall2.redirect_phonecall_view()
        self.assertEqual(result['res_id'], self.phonecall2.id)

    def test_on_change_opportunity(self):
        self.phonecall1.opportunity_id = self.opportunity1
        self.phonecall1.on_change_opportunity()
        self.assertEqual(
            self.phonecall1.partner_phone, self.opportunity1.phone)
        self.assertEqual(self.opportunity1.phonecall_count, 1)

    def test_convert2opportunity(self):
        result = self.phonecall1.action_button_convert2opportunity()
        self.assertEqual(result['res_model'], 'crm.lead')

    def test_make_meeting(self):
        result = self.phonecall1.action_make_meeting()
        self.assertEqual(
            result['context']['default_phonecall_id'], self.phonecall1.id)

    def test_wizard(self):
        model_data = self.env['ir.model.data']
        wizard = self.env['crm.phonecall2phonecall'].with_context(
            active_ids=self.phonecall1.ids, active_id=self.phonecall1.id,
        ).create({})
        result = wizard.action_schedule()
        search_view = model_data.get_object_reference(
            'crm_phonecall', 'view_crm_case_phonecalls_filter')
        self.assertEqual(result['search_view_id'], search_view[1])
