# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, time, timedelta

from odoo import api, models


class ResourceCalendar(models.Model):

    _inherit = 'resource.calendar'

    @api.model
    def _get_conflicting_unavailable_intervals(self, intervals,
                                               start_datetime, end_datetime):
        """ Finds unavailable dt intervals within start_ and end_datetime args

        Args:

            intervals (list): List of tuples containing the AVAILABLE working
                datetimes between the start_datetime and end_datetime values.
                Each tuple contains a start and stop datetime value. Format
                is like so:

                [(start_datetime_1, end_datetime_1),
                 (start_datetime_2, end_datetime_2)]

                The start_datetime and end_datetime values are the start and
                end datetimes of a single available working datetime interval
                (e.g. 2017-03-03 10:00:00 to 2017-03-03 11:00:00)

                The working datetime tuples to be supplied to this method can
                be retrieved like so. Refer to its use in the
                _check_resource_ids_working_times method in calendar.event in
                this module.

                    .. code-block:: python

                    intervals = \
                        resource.calendar_id.get_working_intervals_of_day(
                            start_dt=datetime_start,
                            end_dt=datetime_end,
                            resource_id=resource.id,
                        )

            start_datetime (datetime): Starting point for finding unavailable
                times. An example might be the start datetime of a calendar
                event.

            end_datetime (datetime): Point of which to stop looking for
                unavailable times. An example might be the end or stop
                datetime of a calendar event.

        Returns:
            list: List containing any intervals of which the start
            and end datetimes of those intervals overlap the
            start_datetime and end_datetime args.

        """
        unavailable_intervals = self._get_unavailable_intervals(
            intervals=intervals,
            start_date=start_datetime.date(),
            end_date=end_datetime.date(),
        )

        conflicting_intervals = []
        for interval in unavailable_intervals:

            if all((interval[0] < end_datetime,
                    interval[1] > start_datetime)):
                conflicting_intervals.append(interval)

        return conflicting_intervals

    @api.model
    def _get_unavailable_intervals(self, intervals, start_date, end_date):
        """ Finds any gaps between intervals within start_date and end_date

        Args:

            intervals (list): List of tuples containing the AVAILABLE working
                datetimes between the start_date and end_date. Same format as
                specified in _get_conflicting_unavailable_intervals.

            start_date (date): Starting date with which to look for gaps
                in intervals. An example might be the starting date of
                a calendar event.

            end_date (date): Ending date with which to look for gaps
                in intervals. An example might be the end or stop date
                of a calendar event.`

        """
        start_datetime = datetime.combine(
            start_date, time(00, 00, 00),
        )
        end_datetime = datetime.combine(
            end_date, time(23, 59, 59),
        )

        intervals = self._clean_datetime_intervals(intervals)

        unavailable_intervals = []

        if intervals[0][0] > start_datetime:
            unavailable_intervals.append(
                (start_datetime, intervals[0][0]),
            )

        if intervals[-1][1] < end_datetime:
            unavailable_intervals.append(
                (intervals[-1][1], end_datetime),
            )

        if len(intervals) < 2:
            return unavailable_intervals

        for index, dt_interval in enumerate(intervals):

            if index - 1 < 0:
                continue

            previous_pair = intervals[index - 1]
            if previous_pair[1] < dt_interval[0]:
                unavailable_intervals.append(
                    (previous_pair[1], dt_interval[0]),
                )

        return self._check_round_up_times_to_next_day(
            sorted(unavailable_intervals, key=lambda s: s[0])
        )

    @api.model
    def _clean_datetime_intervals(self, intervals):
        """ Cleans intervals for further analysis.

        Any overlaps in the intervals are fixed and runs
        _check_round_up_times_to_next_day on all the intervals.

        """
        intervals = self._check_round_up_times_to_next_day(
            sorted(intervals, key=lambda s: s[0])
        )

        remove_index = None

        for index, datetime_interval in enumerate(intervals):

            if index - 1 < 0:
                continue

            prev_interval_start = intervals[index - 1][0]
            prev_interval_stop = intervals[index - 1][1]

            interval_start = datetime_interval[0]
            interval_stop = datetime_interval[1]

            if interval_stop <= prev_interval_stop:
                remove_index = index
                break

            if interval_start <= prev_interval_stop:
                intervals[index - 1] = (prev_interval_start, interval_stop)
                remove_index = index
                break

        if remove_index is None:
            return intervals

        del intervals[remove_index]
        return self._clean_datetime_intervals(intervals)

    @api.model
    def _check_round_up_times_to_next_day(self, intervals):
        """ Rounds up eligible datetimes to the next day.

        Any datetimes within 60 seconds of the beginning
        of the next day will be rounded up to the next day.

        The logic applies only to the 2nd item (or index 1)
        in each interval tuple.

        """
        for index, datetime_interval in enumerate(intervals):

            next_day = datetime_interval[1] + timedelta(days=1)

            next_day = next_day.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            if (next_day - datetime_interval[1]).total_seconds() <= 60:
                intervals[index] = (datetime_interval[0], next_day)

        return intervals
