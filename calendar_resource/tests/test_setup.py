# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from mock import patch

from odoo import fields

from .setup import Setup


MOCK_DATETIME = 'odoo.addons.calendar_resource.tests.test_calendar_event.'\
                'fields.Datetime.now'


class TestSetup(Setup):

    @patch(MOCK_DATETIME)
    def test_get_datetime_interval_day_weekday_later(self, mock_datetime):
        """ Ensure returns future weekday later in week """
        mock_datetime.return_value = '2017-06-28 12:00:00'
        res = self._get_datetime_interval(
            3, '12:00:00',
            4, '13:00:00',
        )
        exp = ('2017-08-03 12:00:00', '2017-08-04 13:00:00')
        self.assertEquals(
            res,
            exp,
        )

    @patch(MOCK_DATETIME)
    def test_get_datetime_interval_day_weekday_previous(self, mock_datetime):
        """ Ensure returns future weekday sooner in week """
        mock_datetime.return_value = '2016-05-06 12:00:00'
        res = self._get_datetime_interval(
            0, '12:00:00',
            1, '13:00:00',
        )
        exp = ('2016-06-06 12:00:00', '2016-06-07 13:00:00')
        self.assertEquals(
            res,
            exp,
        )

    @patch(MOCK_DATETIME)
    def test_get_datetime_interval_day_same_weekday(self, mock_datetime):
        """ Ensure returns future weekday same weekday """
        mock_datetime.return_value = '2016-05-02 12:00:00'
        res = self._get_datetime_interval(
            0, '12:00:00',
            0, '13:00:00',
        )
        exp = ('2016-06-06 12:00:00', '2016-06-06 13:00:00')
        self.assertEquals(
            res,
            exp,
        )

    def test_intervals_to_dt(self):
        """ Test changes string to datetime """
        interval = [('2017-03-07 00:00:00', '2017-03-07 16:00:00')]
        exp = [(
            fields.Datetime.from_string(interval[0][0]),
            fields.Datetime.from_string(interval[0][1]),
        )]
        res = self._intervals_to_dt(interval)
        self.assertEquals(
            exp, res
        )
