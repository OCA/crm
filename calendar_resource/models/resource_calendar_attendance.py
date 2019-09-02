# -*- coding: utf-8 -*-
# Copyright 2013 Savoir-faire Linux
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResourceCalendarAttendance(models.Model):

    _inherit = 'resource.calendar.attendance'

    @api.multi
    @api.constrains('date_from', 'date_to')
    def _check_date_from_date_to(self):
        for record in self:
            conditions = (
                record.date_to and record.date_from,
                record.date_to < record.date_from,
            )
            if all(conditions):
                raise ValidationError(_(
                    'End Date cannot be earlier '
                    'than Starting Date.',
                ))

    @api.multi
    @api.constrains('hour_from', 'hour_to')
    def _check_hour_from_hour_to(self):
        for record in self:
            if record.hour_to <= record.hour_from:
                raise ValidationError(_(
                    'Work to cannot be earlier or the same '
                    'as Work from. If it is a night '
                    'shift, separate the hours into their '
                    'own working time entries by weekday.',
                ))
