# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields

from .setup import Setup


class TestResourceCalendar(Setup):

    def test_get_unavailable_intervals_outside_both(self):
        """ Test returns intervals event outside both """
        start = fields.Datetime.from_string('2017-03-06 00:00:00')
        end = fields.Datetime.from_string('2017-03-12 23:59:59')
        exp = [
            ('2017-03-06 00:00:00', '2017-03-07 00:00:00'),
            ('2017-03-08 16:00:00', '2017-03-09 09:00:00'),
            ('2017-03-10 00:00:00', '2017-03-13 00:00:00'),
        ]
        exp = self._intervals_to_dt(exp)
        self.assertEquals(
            exp,
            self.Calendar._get_unavailable_intervals(
                self.intervals,
                start.date(),
                end.date(),
            )
        )

    def test_get_conflicting_intervals_inside_both(self):
        """ Test returns intervals event inside both """
        start = fields.Datetime.from_string('2017-03-08 17:00:00')
        end = fields.Datetime.from_string('2017-03-09 08:00:00')
        exp = [
            ('2017-03-08 16:00:00', '2017-03-09 09:00:00'),
        ]
        exp = self._intervals_to_dt(exp)
        self.assertEquals(
            exp,
            self.Calendar._get_conflicting_unavailable_intervals(
                self.intervals,
                start,
                end,
            )
        )

    def test_get_conflicting_intervals_overlap_inside_left(self):
        """ Test returns intervals event overlap left """
        start = fields.Datetime.from_string('2017-03-07 10:00:00')
        end = fields.Datetime.from_string('2017-03-09 06:00:00')
        exp = [
            ('2017-03-08 16:00:00', '2017-03-09 09:00:00'),
        ]
        exp = self._intervals_to_dt(exp)
        self.assertEquals(
            exp,
            self.Calendar._get_conflicting_unavailable_intervals(
                self.intervals,
                start,
                end,
            )
        )

    def test_get_conflicting_intervals_overlap_outside_left(self):
        """ Test returns intervals event overlap left """
        start = fields.Datetime.from_string('2017-03-06 10:00:00')
        end = fields.Datetime.from_string('2017-03-07 06:00:00')
        exp = [
            ('2017-03-06 00:00:00', '2017-03-07 00:00:00'),
        ]
        exp = self._intervals_to_dt(exp)
        self.assertEquals(
            exp,
            self.Calendar._get_conflicting_unavailable_intervals(
                self.intervals,
                start,
                end,
            )
        )

    def test_get_unavailable_intervals_match_right(self):
        """ Test returns intervals event match right """
        start = fields.Datetime.from_string('2017-03-09 09:00:00')
        end = fields.Datetime.from_string('2017-03-10 00:00:00')
        exp = [
            ('2017-03-08 16:00:00', '2017-03-09 09:00:00'),
            ('2017-03-10 00:00:00', '2017-03-11 00:00:00'),
        ]
        exp = self._intervals_to_dt(exp)
        self.assertEquals(
            exp,
            self.Calendar._get_unavailable_intervals(
                self.intervals,
                start,
                end,
            )
        )

    def test_get_conflicting_intervals_match_right(self):
        """ Test returns intervals event match right """
        start = fields.Datetime.from_string('2017-03-09 09:00:00')
        end = fields.Datetime.from_string('2017-03-10 00:00:00')
        self.assertFalse(
            self.Calendar._get_conflicting_unavailable_intervals(
                self.intervals,
                start,
                end,
            )
        )

    def test_clean_datetime_intervals(self):
        """ Test overlaps correctly removed """
        res = self.Calendar._clean_datetime_intervals(self.intervals)
        exp = self.cleaned_intervals
        self.assertEquals(
            res,
            exp,
            'Intervals are not equal.\nRes:\n%s\nExpect:\n%s' % (res, exp),
        )
