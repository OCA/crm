# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields
import openerp.tests.common as common


class TestCrmMeetingCommercialPartner(common.TransactionCase):

    def setUp(self):
        super(TestCrmMeetingCommercialPartner, self).setUp()
        self.calendar_event_model = self.env['calendar.event']
        self.partner_company = self.env['res.partner'].create({
            'name': 'Company',
            'is_company': True,
        })
        self.partner_contact_1 = self.env['res.partner'].create({
            'name': 'Contact 1',
            'is_company': False,
            'parent_id': self.partner_company.id,
        })
        self.partner_contact_2 = self.env['res.partner'].create({
            'name': 'Contact 1',
            'is_company': False,
            'parent_id': self.partner_company.id,
        })

    def test_meetings(self):
        self.calendar_event_model.create({
            'name': 'Meeting with contact 1',
            'allday': True,
            'start_date': fields.Date.today(),
            'stop_date': fields.Date.today(),
            'partner_ids': [(6, 0, self.partner_contact_1.ids)],
        })
        self.calendar_event_model.create({
            'name': 'Meeting with contact 1',
            'allday': True,
            'start_date': fields.Date.today(),
            'stop_date': fields.Date.today(),
            'partner_ids': [(6, 0, self.partner_contact_2.ids)],
        })
        self.calendar_event_model.create({
            'name': 'Meeting with company',
            'allday': True,
            'start_date': fields.Date.today(),
            'stop_date': fields.Date.today(),
            'partner_ids': [(6, 0, self.partner_company.ids)],
        })
        # We cannot test the meeting_count in v9. We'll do in v10
        # self.assertEqual(self.partner_company.meeting_count, 3)
        action = self.partner_company.with_context(
            partner_name=self.partner_company.name).schedule_meeting()
        partners = self.partner_company + self.partner_contact_1 + \
            self.partner_contact_2
        self.assertEquals(
            sorted(action['context']['search_default_partner_ids']),
            sorted(partners.ids))
