# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestCrmPhoneCall(common.SavepointCase):
    """Unit test case of the Crm Phonecall module."""

    @classmethod
    def setUpClass(cls):
        """Created required data."""
        super(TestCrmPhoneCall, cls).setUpClass()
        cls.company = cls.env.ref('base.main_company')
        partner_obj = cls.env['res.partner']
        cls.campaign1 = cls.env['utm.campaign'].create({
            "name": "campaign 1",
        })
        cls.source1 = cls.env['utm.source'].create({
            "name": "source 1",
        })
        cls.medium1 = cls.env['utm.medium'].create({
            "name": "medium 1",
        })
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
            'campaign_id': cls.campaign1.id,
            'source_id': cls.source1.id,
            'medium_id': cls.medium1.id,
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
        """Partner change method test."""
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
        """Schedule another phonecall."""
        phonecall2 = self.phonecall1.schedule_another_phonecall(
            schedule_time=False,
            call_summary='Test schedule method',
            action='schedule',
            tag_ids=self.tag.ids,
        )[self.phonecall1.id]
        self.assertNotEqual(phonecall2.id, self.phonecall1.id)
        self.assertEqual(self.phonecall1.state, 'open')
        phonecall3 = self.phonecall1.schedule_another_phonecall(
            schedule_time='2017-12-31 00:00:00',
            call_summary='Test schedule method2',
            action='log',
        )[self.phonecall1.id]
        self.assertNotEqual(phonecall3.id, self.phonecall1.id)
        self.assertNotEqual(phonecall3.id, phonecall2.id)
        self.assertEqual(self.phonecall1.state, 'done')
        result = phonecall2.redirect_phonecall_view()
        self.assertEqual(result['res_id'], phonecall2.id)
        for phonecall in (self.phonecall1, phonecall2, phonecall3):
            self.assertEqual(phonecall.campaign_id, self.campaign1)
            self.assertEqual(phonecall.source_id, self.source1)
            self.assertEqual(phonecall.medium_id, self.medium1)

    def test_on_change_opportunity(self):
        """Change the opportunity."""
        self.phonecall1.opportunity_id = self.opportunity1
        self.phonecall1.on_change_opportunity()
        self.assertEqual(
            self.phonecall1.partner_phone, self.opportunity1.phone)
        self.assertEqual(self.opportunity1.phonecall_count, 1)

    def test_convert2opportunity(self):
        """Convert lead to opportunity test."""
        result = self.phonecall1.action_button_convert2opportunity()
        self.assertEqual(result['res_model'], 'crm.lead')
        lead = self.env["crm.lead"].browse(result["res_id"])
        self.assertEqual(lead.campaign_id, self.campaign1)
        self.assertEqual(lead.source_id, self.source1)
        self.assertEqual(lead.medium_id, self.medium1)

    def test_make_meeting(self):
        """Make a meeting test."""
        result = self.phonecall1.action_make_meeting()
        self.assertEqual(
            result['context']['default_phonecall_id'], self.phonecall1.id)

    def test_wizard(self):
        """Schedule a call from wizard."""
        model_data = self.env['ir.model.data']
        wizard = self.env['crm.phonecall2phonecall'].with_context(
            active_ids=self.phonecall1.ids, active_id=self.phonecall1.id,
        ).create({})
        result = wizard.action_schedule()
        search_view = model_data.get_object_reference(
            'crm_phonecall', 'view_crm_case_phonecalls_filter')
        self.assertEqual(result['search_view_id'], search_view[1])
        self.assertNotEqual(result['res_id'], self.phonecall1.id)

    def test_opportunity_open_phonecall(self):
        action_dict = self.opportunity2.button_open_phonecall()
        action_context = action_dict.get('context')
        self.assertEqual(action_context.get('default_opportunity_id'),
                         self.opportunity2.id)
        self.assertEqual(action_context.get('search_default_opportunity_id'),
                         self.opportunity2.id)
        self.assertEqual(action_context.get('default_partner_id'),
                         self.opportunity2.partner_id.id)
