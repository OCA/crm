# -*- coding: utf-8 -*-
# Copyright 2013 Savoir-faire Linux
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from os import linesep
from datetime import datetime, time, timedelta
from dateutil.rrule import rrule, DAILY

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    resource_ids = fields.Many2many(
        string='Resources',
        comodel_name='resource.resource',
    )

    @api.model
    def _format_datetime_intervals_to_str(self, intervals):
        """ Converts intervals to string values.

        Example:

            .. code-block python

            self._format_datetime_intervals_to_str(
                intervals=[
                    (
                        datetime(2017, 6, 28, 17, 0, 0),
                        datetime(2017, 6, 29, 8, 0, 0),
                    ),
                    (
                        datetime(2017, 6, 29, 12, 0, 0),
                        datetime(2017, 6, 29, 13, 0, 0),
                    ),
                ],
            )

            The above example will output the following string,
            depending on date and time format, as well as timezone.

            \n06/28/2017 at 17:00:00 To\n
            06/29/2017 at 08:00:00 (UTC)\n

            \n06/29/2017 at 12:00:00 To\n
            06/29/2017 at 13:00:00 (UTC)\n

        Returns:

            (str): string formatted for front-end
            display purposes, taking into account language, timezone, as
            well as date and time formats.

        """
        datetimes = []
        for interval in intervals:
            if not isinstance(interval[0], basestring):
                interval = (
                    fields.Datetime.to_string(interval[0]),
                    fields.Datetime.to_string(interval[1]),
                )
            args = {
                'start': interval[0],
                'stop': interval[1],
                'zallday': False,
                'zduration': 24,
            }
            datetimes.append(self._get_display_time(**args))
        return (2 * linesep).join(datetimes)

    @api.multi
    def _event_in_past(self):
        self.ensure_one()
        stop_datetime = fields.Datetime.from_string(self.stop)
        now_datetime = datetime.now()
        return stop_datetime < now_datetime

    @api.multi
    @api.constrains('resource_ids', 'start', 'stop')
    def _check_resource_ids_double_book(self):

        for record in self:

            if record._event_in_past():
                continue

            resources = record.resource_ids.filtered(
                lambda s: s.allow_double_book is False
            )

            if not any(resources):
                continue

            overlaps = self.env['calendar.event'].search([
                ('id', '!=', record.id),
                ('start', '<', record.stop),
                ('stop', '>', record.start),
            ])

            for resource in overlaps.mapped(lambda s: s.resource_ids):
                raise ValidationError(
                    _(
                        'The resource, %s, cannot be double-booked '
                        'with any overlapping meetings or events.',
                    )
                    % resource.name,
                )

    @api.multi
    @api.constrains('resource_ids', 'categ_ids')
    def _check_resource_ids_categ_ids(self):

        for record in self:

            if record._event_in_past():
                continue

            if not record.categ_ids:
                continue

            for resource in record.resource_ids:
                categs = record.categ_ids.filtered(
                    lambda s: s not in resource.allowed_event_types
                )
                if categs:
                    raise ValidationError(
                        _(
                            "The resource, '%s', is not allowed in the "
                            "following event types: \n%s",
                        )
                        % (
                            resource.name,
                            ', '.join([
                                categ.name for categ in categs
                            ]),
                        )
                    )

    @api.multi
    @api.constrains('resource_ids', 'start', 'stop')
    def _check_resource_ids_leaves(self):

        for record in self:

            if record._event_in_past():
                continue

            for resource in record.resource_ids:

                if not resource.calendar_id:
                    continue

                if not resource.calendar_id.leave_ids:
                    continue

                conflict_leaves = resource.calendar_id.leave_ids.filtered(
                    lambda s: s.date_from < record.stop and
                    s.date_to > record.start
                )

                if not conflict_leaves:
                    continue

                datetimes = [(c.date_from, c.date_to) for c in conflict_leaves]
                raise ValidationError(
                    _(
                        "The resource, '%s', is on leave during "
                        "the following times which are conflicting with "
                        "this event.\n%s",
                    )
                    % (
                        resource.name,
                        self._format_datetime_intervals_to_str(datetimes),
                    )
                )

    @api.multi
    def _get_event_date_list(self):
        """ Builds a list of datetimes of the days of the event

        Each datetime in the list is the beginning of a
        separate day.

        """
        self.ensure_one()
        start_date = fields.Date.from_string(self.start)
        stop_datetime = fields.Datetime.from_string(self.stop)

        if stop_datetime.time() == time(0, 0):
            stop_datetime -= timedelta(days=1)

        return list(
            rrule(DAILY, dtstart=start_date, until=stop_datetime.date())
        )

    @api.multi
    @api.constrains('resource_ids', 'start', 'stop')
    def _check_resource_ids_working_times(self):

        for record in self:

            if record._event_in_past():
                continue

            event_start = fields.Datetime.from_string(record.start)
            event_stop = fields.Datetime.from_string(record.stop)

            event_days = record._get_event_date_list()

            for resource in record.resource_ids.filtered(
                    lambda s: s.calendar_id):

                available_intervals = []
                conflict_intervals = []

                for day in event_days:

                    datetime_start = datetime.combine(day, time(00, 00, 00))
                    datetime_end = datetime.combine(day, time(23, 59, 59))

                    intervals = \
                        resource.calendar_id.get_working_intervals_of_day(
                            start_dt=datetime_start,
                            end_dt=datetime_end,
                            resource_id=resource.id,
                        )

                    if not intervals:
                        conflict_intervals.append(
                            (datetime_start, datetime_end),
                        )
                    else:
                        available_intervals += intervals

                ResourceCalendar = self.env['resource.calendar']

                if available_intervals and not record.allday:
                    conflict_intervals = ResourceCalendar.\
                        _get_conflicting_unavailable_intervals(
                            available_intervals, event_start, event_stop,
                        )

                if not conflict_intervals:
                    continue

                conflict_intervals = ResourceCalendar.\
                    _clean_datetime_intervals(
                        conflict_intervals,
                    )

                raise ValidationError(
                    _(
                        'The resource, %s, is not available during '
                        'the following dates and times which are '
                        'conflicting with the event:%s%s',
                    )
                    % (
                        resource.name,
                        2 * linesep,
                        self._format_datetime_intervals_to_str(
                            conflict_intervals,
                        ),
                    )
                )
