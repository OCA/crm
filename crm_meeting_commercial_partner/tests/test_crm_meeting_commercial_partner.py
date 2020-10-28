# Author: Jordi Ballester Alomar
# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common
from odoo import fields


class TestCrmMeetingCommercialPartner(common.TransactionCase):
    def setUp(self):
        super(TestCrmMeetingCommercialPartner, self).setUp()
        self.calendar_event_model = self.env["calendar.event"]
        self.partner_company = self.env["res.partner"].create(
            {"name": "Company", "is_company": True}
        )
        self.partner_contact_1 = self.env["res.partner"].create(
            {
                "name": "Contact 1",
                "is_company": False,
                "parent_id": self.partner_company.id,
            }
        )
        self.partner_contact_2 = self.env["res.partner"].create(
            {
                "name": "Contact 1",
                "is_company": False,
                "parent_id": self.partner_company.id,
            }
        )

    def test_meetings(self):
        self.calendar_event_model.create(
            {
                "name": "Meeting with contact 1",
                "allday": True,
                "start": fields.Datetime.now(),
                "stop": fields.Datetime.now(),
                "partner_ids": [(6, 0, self.partner_contact_1.ids)],
            }
        )
        self.calendar_event_model.create(
            {
                "name": "Meeting with contact 1",
                "allday": True,
                "start": fields.Datetime.now(),
                "stop": fields.Datetime.now(),
                "partner_ids": [(6, 0, self.partner_contact_1.ids)],
            }
        )
        self.calendar_event_model.create(
            {
                "name": "Meeting with contact 1",
                "allday": True,
                "start": fields.Datetime.now(),
                "stop": fields.Datetime.now(),
                "partner_ids": [(6, 0, self.partner_contact_2.ids)],
            }
        )
        self.calendar_event_model.create(
            {
                "name": "Meeting with company",
                "allday": True,
                "start": fields.Datetime.now(),
                "stop": fields.Datetime.now(),
                "partner_ids": [(6, 0, self.partner_company.ids)],
            }
        )
        self.assertEqual(self.partner_company.meeting_count, 4)
        self.assertEqual(self.partner_contact_1.meeting_count, 2)
        action = self.partner_company.with_context(
            partner_name=self.partner_company.name
        ).schedule_meeting()
        partners = (
            self.partner_company + self.partner_contact_1 + self.partner_contact_2
        )
        res = (
            self.calendar_event_model.search(action["domain"]).mapped("partner_ids").ids
        )
        self.assertEquals(sorted(res), sorted(partners.ids))
