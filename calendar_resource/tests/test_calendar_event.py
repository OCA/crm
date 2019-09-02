# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from mock import patch

from odoo import fields
from odoo.exceptions import ValidationError

from .setup import Setup
from .setup import MOCK_FORMATS


class TestCalendarEvent(Setup):

    def test_overlap_left_outside_date_allow_double_book_true(self):
        """ Test overlap date no raise Validation if allow_double_book True """
        self.resource_1.allow_double_book = True
        self._create_event()
        start_stop = self._get_datetime_interval(
            0, '00:00:00',
            2, '00:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
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
        self._create_event()
        start_stop = self._get_datetime_interval(
            1, '11:00:00',
            1, '12:30:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if allow_double_book is True'
            )

    def test_overlap_left_outside_date(self):
        """ Test left side overlap raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            0, '00:00:00',
            2, '00:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_overlap_right_outside_date(self):
        """ Test right side overlap raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            2, '00:00:00',
            4, '00:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_match_left_outside_date(self):
        """ Test left side match not ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            0, '00:00:00',
            1, '12:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if stop datetime same as existing event '
                'start datetime',
            )

    def test_match_right_outside_date(self):
        """ Test date right side match not ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            3, '14:00:00',
            4, '00:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if start datetime same as existing event '
                'stop datetime',
            )

    def test_overlap_both_inside_time(self):
        """ Test time overlap both inside raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            2, '00:00:00',
            2, '10:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_match_both_inside_date(self):
        """ Test date match both inside raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            1, '12:00:00',
            3, '14:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_overlap_both_outside_date(self):
        """ Test date overlap both outside raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            0, '00:00:00',
            4, '00:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_overlap_left_outside_time(self):
        """ Test time left side overlap raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            1, '00:00:00',
            1, '12:30:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_overlap_right_outside_time(self):
        """ Test time right side overlap raise ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            3, '13:00:00',
            3, '15:30:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_match_left_outside_time(self):
        """ Test time left side match not ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            1, '00:00:00',
            1, '12:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if stop time same as existing event '
                'start time',
            )

    def test_match_right_outside_time(self):
        """ Test time date right side match not ValidationError """
        self._create_event()
        start_stop = self._get_datetime_interval(
            3, '14:00:00',
            3, '16:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if start time same as existing event '
                'stop time',
            )

    def test_check_resource_ids_categ_ids_raise_error(self):
        """ Test raise ValidationError if resource not allowed """
        existing_event = self._create_event()
        with self.assertRaises(ValidationError):
            existing_event.write({
                'resource_ids': [(4, [self.resource_2.id])],
                'categ_ids': [(4, [self.event_type_5.id])],
            })

    def test_check_resource_ids_categ_ids_no_error(self):
        """ Test no error if allowed resource added """
        existing_event = self._create_event()
        try:
            existing_event.write({
                'resource_ids': [(4, [self.resource_2.id])],
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise validation error if '
                'eligible resource added.'
            )

    def test_check_resource_ids_categ_ids_no_error_resource(self):
        """ Test no error if allowed resource added when no categ """
        existing_event = self._create_event()
        existing_event.write({
            'categ_ids': [(5, 0, 0)],
            'resource_ids': [(5, 0, 0)],
        })
        try:
            existing_event.write({
                'resource_ids': [(4, [self.resource_2.id])],
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise validation error if '
                'eligible resource added.'
            )

    def test_check_resource_ids_categ_ids_no_error_categ(self):
        """ Test no error if allowed categ added when no resource """
        existing_event = self._create_event()
        existing_event.write({
            'categ_ids': [(5, 0, 0)],
            'resource_ids': [(5, 0, 0)],
        })
        try:
            existing_event.write({
                'categ_ids': [(4, [self.event_type_4.id])],
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise validation error if '
                'eligible categ added.'
            )

    def test_event_in_past_true(self):
        """ Test returns true if event in past """
        event = self._create_event({
            'start': '2016-06-01 00:00:00',
            'stop': '2016-06-02 00:00:00',
        })
        self.assertTrue(
            event._event_in_past()
        )

    def test_event_in_past_false(self):
        """ Test returns false if event in future """
        event = self._create_event()
        self.assertFalse(
            event._event_in_past()
        )

    def test_check_resource_leaves_datetime_in_past(self):
        """ Test no validationerror if event in the past """
        self.leave_1.write({
            'date_from': '2015-04-10 12:00:00',
            'date_to': '2015-05-12 14:00:00',
        })
        try:
            self._create_event({
                'start': '2015-04-10 12:00:00',
                'stop': '2015-05-12 12:00:00',
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError if event in past'
            )

    def test_check_resource_leaves_resource_no_calendar(self):
        """ Test no validationerror if resource has no calendar_id """
        self.resource_1.calendar_id = None
        start_stop = self._get_datetime_interval(
            0, '12:00:00',
            6, '20:00:00'
        )
        self.leave_1.write({
            'date_from': start_stop[0],
            'date_to': start_stop[1],
        })
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError if resource '
                'has no calendar_id'
            )

    def test_check_resource_leaves(self):
        """ Test raise ValidationError if conflicting leave """
        start_stop = self._get_datetime_interval(
            1, '12:00:00',
            3, '12:00:00'
        )
        self.leave_1.write({
            'date_from': start_stop[0],
            'date_to': start_stop[1],
        })
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
            })

    @patch(MOCK_FORMATS)
    def test_format_datetime_intervals_to_str(self, datetime_format):
        """ Test returns correct string """
        datetime_format.return_value = ('%Y-%m-%d', '%H:%M:%S')
        intervals = [
            ('2017-03-07 00:00:00', '2017-03-07 16:00:00'),
            ('2017-03-07 12:00:00', '2017-03-07 20:00:00'),
        ]
        intervals_dt = self._intervals_to_dt([
            ('2017-03-07 00:00:00', '2017-03-07 16:00:00'),
            ('2017-03-07 12:00:00', '2017-03-07 20:00:00'),
        ])

        args = {
            'start': intervals[0][0],
            'stop': intervals[0][1],
            'zallday': False,
            'zduration': 24,
        }
        intervals[0] = self.Event._get_display_time(**args)
        args.update({
            'start': intervals[1][0],
            'stop': intervals[1][1],
        })
        intervals[1] = self.Event._get_display_time(**args)

        exp = '%s\n\n%s' % (intervals[0], intervals[1])
        res = self.Event._format_datetime_intervals_to_str(intervals_dt)

        self.assertEquals(
            exp, res,
        )

    def test_check_resource_ids_working_times_past(self):
        """ Test no validationerror if event in past """
        self.resource_1.calendar_id = self.calendar_1
        try:
            self._create_event({
                'start': '2017-03-06 00:00:00',
                'stop': '2017-03-12 00:00:00',
                'allday': False,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not fail if event in past'
            )

    def test_check_resource_ids_working_times_overlap_left(self):
        """ Test ValidationError if event overlapping unavailable times """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            0, '23:00:00',
            2, '20:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': False,
            })

    def test_check_resource_ids_working_times_match_left(self):
        """ Test no Error if event stop is unavailable time start """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            1, '00:00:00',
            2, '16:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': False,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise Error if event stop matches '
                'unavailable time start'
            )

    def test_check_resource_ids_working_times_inside_left(self):
        """ Test no Error if event within working times """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            1, '00:00:00',
            2, '10:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': False,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise Error if event witin working times'
            )

    def test_check_resource_ids_working_times_overlap_right(self):
        """ Test ValidationError if event overlapping unavailable times """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            3, '00:00:00',
            5, '20:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': False,
            })

    def test_check_resource_ids_working_times_match_right(self):
        """ Test no Error if event stop is unavailable time start """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            3, '09:00:00',
            4, '00:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': False,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise Error if event stop matches '
                'unavailable time start'
            )

    def test_check_resource_ids_working_times_right_whole_day(self):
        """ Test ValidationError if event on non-working day """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            5, '09:00:00',
            6, '00:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': False,
            })

    def test_check_resource_ids_working_times_right_whole_day_allday(self):
        """ Test ValidationError if allday event on non-working day """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            5, '00:00:00',
            6, '00:00:00',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_check_resource_ids_working_times_right_week_allday(self):
        """ Test ValidationError if allday event all week """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            0, '00:00:00',
            6, '23:59:59',
        )
        with self.assertRaises(ValidationError):
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })

    def test_check_resource_ids_working_times_allday_overlap_outside(self):
        """ Test no Error if allday event is on day with 1+ working time """
        self.resource_1.calendar_id = self.calendar_1
        start_stop = self._get_datetime_interval(
            2, '00:00:00',
            4, '00:00:00',
        )
        try:
            self._create_event({
                'start': start_stop[0],
                'stop': start_stop[1],
                'allday': True,
            })
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise Error if event is allday '
                'and there is at least 1 working interval that day '
            )

    def test_get_event_date_list(self):
        event = self._create_event({
            'start': '2016-06-01 00:00:00',
            'stop': '2016-06-03 00:00:00',
        })
        exp = [
            fields.Datetime.from_string('2016-06-01 00:00:00'),
            fields.Datetime.from_string('2016-06-02 00:00:00'),
        ]
        self.assertEquals(
            exp,
            event._get_event_date_list()
        )
