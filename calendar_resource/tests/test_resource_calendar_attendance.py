# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestResourceCalendarAttendance(TransactionCase):

    def setUp(self):
        super(TestResourceCalendarAttendance, self).setUp()
        self.attendance_1 = self.env.ref(
            'resource.calendar_attendance_mon1'
        )

    def test_check_date_from_date_to(self):
        """ Test raise ValidationError if dates not in order """
        with self.assertRaises(ValidationError):
            self.attendance_1.write({
                'date_from': fields.Date.from_string('2016-06-06'),
                'date_to': fields.Date.from_string('2016-05-05'),
            })

    def test_check_hour_from_hour_to(self):
        """ Test raise ValidationError if hours not in order """
        with self.assertRaises(ValidationError):
            self.attendance_1.write({
                'hour_from': 5.00,
                'hour_to': 4.00,
            })
