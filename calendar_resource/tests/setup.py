# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


MOCK_FORMATS = 'odoo.addons.calendar.models.calendar.Meeting.'\
               '_get_date_formats'


class Setup(TransactionCase):

    def setUp(self):
        super(Setup, self).setUp()
        self.resource_1 = self.env.ref('resource.resource_analyst')
        self.resource_2 = self.env.ref('resource.resource_designer')
        self.calendar_1 = self.env.ref('calendar_resource.resource_calendar_1')

        self.resource_1.allow_double_book = False

        self.event_type_4 = self.env.ref('calendar.categ_meet4')
        self.event_type_5 = self.env.ref('calendar.categ_meet5')

        self.leave_1 = self.env.ref(
            'resource.resource_analyst_leaves_demoleave1'
        )

        self.env.user.partner_id.tz = 'UTC'
        self.env.user.lang = 'en_US'

        self.Calendar = self.env['resource.calendar']
        self.Event = self.env['calendar.event']

        self.intervals = [
            ('2017-03-07 00:00:00', '2017-03-07 16:00:00'),
            ('2017-03-07 12:00:00', '2017-03-07 20:00:00'),
            ('2017-03-07 20:00:00', '2017-03-07 23:59:59'),
            ('2017-03-08 00:00:00', '2017-03-08 16:00:00'),
            ('2017-03-08 05:00:00', '2017-03-08 11:30:00'),
            ('2017-03-09 09:00:00', '2017-03-09 23:59:00'),
        ]
        self.intervals = self._intervals_to_dt(self.intervals)

        # self.intervals are the same weekdays as the demo
        # attendances tied to demo data id: resource_calendar_1

        # 2017-03-06: Monday
        # 2017-03-07: Tuesday
        # 2017-03-08: Wednesday
        # 2017-03-09: Thursday
        # 2017-03-10: Friday
        # 2017-03-11: Saturday
        # 2017-03-12: Sunday

        # Overlaps removed and days rounded up
        self.cleaned_intervals = [
            ('2017-03-07 00:00:00', '2017-03-08 16:00:00'),
            ('2017-03-09 09:00:00', '2017-03-10 00:00:00'),
        ]
        self.cleaned_intervals = self._intervals_to_dt(
            self.cleaned_intervals,
        )

        self.unavailable_intervals = [
            ('2017-03-06 00:00:00', '2017-03-07 00:00:00'),
            ('2017-03-08 16:00:00', '2017-03-09 09:00:00'),
            ('2017-03-10 00:00:00', '2017-03-13 00:00:00'),
        ]
        self.unavailable_intervals = self._intervals_to_dt(
            self.unavailable_intervals,
        )

    def _intervals_to_dt(self, intervals):
        """ Converts all intervals from string values to datetime.

        Args:
            intervals (list): List of tuples each containing
                a start and stop string value to be converted
                to datetime.

        """
        for index, interval in enumerate(intervals):
            intervals[index] = (
                fields.Datetime.from_string(interval[0]),
                fields.Datetime.from_string(interval[1]),
            )
        return intervals

    def _get_datetime_interval(self, start_weekday, start_time,
                               end_weekday, end_time):
        """ Use this method to ensure events are always in the future

        Note that the event start and stop dates will always be the same
        days of the week as your start_weekday and end_weekday values.

        Args:

            start_weekday (int): Day of the week the event should start.

            start_time (str): Time of day for start_weekday in format:
                '00:00:00' or '%H:%M:%S'.

            end_weekday (int): Day of the week the event should end on.

            end_time (str): Time of day for end_weekday in format:
                '00:00:00' or '%H:%M:%S'.

        Example:

            .. code-block python

            start_stop = self._get_datetime_interval(
                1, '00:00:00',
                2, '16:00:00',
            )

        Returns:

            tuple: A tuple with index 0 as the start_datetime, and index
            1 as the end_datetime.

        """
        start_date = fields.Date.from_string(
            fields.Datetime.now()
        )

        # 35 = 5 weeks * 7 days per week
        # done to avoid demo resource leaves
        # that may be in the same month
        start_date += timedelta(days=35)

        time_format = '%H:%M:%S'
        start_time = datetime.strptime(start_time, time_format).time()
        end_time = datetime.strptime(end_time, time_format).time()

        if not start_date.weekday() == 0:
            while start_date.weekday() != 0:
                start_date -= timedelta(days=1)

        while start_date.weekday() != start_weekday:
            start_date += timedelta(days=1)

        end_date = start_date
        while end_date.weekday() != end_weekday:
            end_date += timedelta(days=1)

        start_datetime = fields.Datetime.to_string(
            datetime.combine(start_date, start_time)
        )
        end_datetime = fields.Datetime.to_string(
            datetime.combine(end_date, end_time)
        )

        return (start_datetime, end_datetime)

    def _create_event(self, vals=None):
        create_vals = {
            'name': 'Test Event',
            'resource_ids': [(6, 0, [self.resource_1.id])],
            'categ_ids': [(6, 0, [self.event_type_4.id])],
            'allday': True,
        }
        if vals:
            create_vals.update(vals)

        if 'start' not in create_vals:
            start_stop = self._get_datetime_interval(
                1, '12:00:00',
                3, '14:00:00',
            )
            create_vals.update({
                'start': start_stop[0],
                'stop': start_stop[1],
            })
        return self.env['calendar.event'].create(create_vals)
