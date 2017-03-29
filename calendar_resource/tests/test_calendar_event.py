# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCalendarEvent(TransactionCase):

    def setUp(self):
        super(TestCalendarEvent, self).setUp()
        self.resource_1 = self.env.ref('resource.resource_analyst')
        self.resource_1.allow_double_book = False
        self.event_1 = self._create_event()

    def _create_event(self, vals=None):
        create_vals = {
            'name': 'Test Event',
            'start': '2016-05-10 12:00:00',
            'stop': '2016-05-12 14:00:00',
            'resource_ids': [(6, 0, [self.resource_1.id])],
        }
        if vals:
            create_vals.update(vals)
        return self.env['calendar.event'].create(create_vals)

    def test_overlap_left_outside_date_allow_double_book_true(self):
        """ Test overlap date no raise Validation if allow_double_book True """
        self.resource_1.allow_double_book = True
        try:
            self._create_event({
                'start': '2016-05-09 00:00:00',
                'stop': '2016-05-12 00:00:00',
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if allow_double_book is True'
            )

    def test_overlap_left_outside_time_allow_double_book_true(self):
        """ Test overlap time no raise Validation allow_dbl_book True """
        self.resource_1.allow_double_book = True
        try:
            self._create_event({
                'start': '2016-05-10 11:00:00',
                'stop': '2016-05-10 13:00:00',
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if allow_double_book is True'
            )

    def test_overlap_left_outside_date(self):
        """ Test left side overlap raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-09 00:00:00',
                'stop': '2016-05-11 00:00:00',
            })

    def test_overlap_right_outside_date(self):
        """ Test right side overlap raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-11 00:00:00',
                'stop': '2016-05-13 00:00:00',
            })

    def test_match_left_outside_date(self):
        """ Test left side match not ValidationError """
        try:
            self._create_event({
                'start': '2016-05-09 00:00:00',
                'stop': '2016-05-10 12:00:00',
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if stop datetime same as self.event_1 '
                'start datetime',
            )

    def test_match_right_outside_date(self):
        """ Test date right side match not ValidationError """
        try:
            self._create_event({
                'start': '2016-05-12 14:00:00',
                'stop': '2016-05-13 00:00:00',
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if start datetime same as self.event_1 '
                'stop datetime',
            )

    def test_overlap_both_inside_time(self):
        """ Test time overlap both inside raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-11 00:00:00',
                'stop': '2016-05-11 08:00:00',
            })

    def test_match_both_inside_date(self):
        """ Test date match both inside raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-10 12:00:00',
                'stop': '2016-05-12 14:00:00',
            })

    def test_overlap_both_outside_date(self):
        """ Test date overlap both outside raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-10 12:00:00',
                'stop': '2016-05-12 14:00:00',
            })

    def test_overlap_left_outside_time(self):
        """ Test time left side overlap raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-10 08:00:00',
                'stop': '2016-05-11 00:00:00',
            })

    def test_overlap_right_outside_time(self):
        """ Test time right side overlap raise ValidationError """
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': '2016-05-11 00:00:00',
                'stop': '2016-05-12 16:00:00',
            })

    def test_match_left_outside_time(self):
        """ Test time left side match not ValidationError """
        try:
            self._create_event({
                'start': '2016-05-10 10:00:00',
                'stop': '2016-05-10 12:00:00',
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if stop time same as self.event_1 '
                'start time',
            )

    def test_match_right_outside_time(self):
        """ Test time date right side match not ValidationError """
        try:
            self._create_event({
                'start': '2016-05-12 14:00:00',
                'stop': '2016-05-12 16:00:00',
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if start time same as self.event_1 '
                'stop time',
            )
