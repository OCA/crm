# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'

    from_days = fields.Integer(
        string='From days',
        help='Anticipation days from date begin or date end', default=0)
    estimated_days = fields.Integer(
        string='Estimated days', help='Estimated days to end', default=1)

    def count_days_without_weekend(self, date_start, date_end):
        days = (date_end - date_start).days
        return sum(1 for x in xrange(days)
                   if (date_start + timedelta(x + 1)).weekday() < 5)

    def count_days_weekend(self, date_start, date_end):
        days = (date_end - date_start).days
        return sum(1 for x in xrange(days)
                   if (date_start + timedelta(x + 1)).weekday() >= 5)

    def correct_days_to_workable(self, date, increment=True):
        while date.weekday() >= 5:
            if increment:
                date += timedelta(days=1)
            else:
                date -= timedelta(days=1)
        return date

    def calculate_date_without_weekend(self, date_start, days, increment=True):
        if increment:
            start = date_start
            end = date_start + timedelta(days=days)
        else:
            start = date_start - timedelta(days=days)
            end = date_start
        holidays = self.count_days_weekend(start, end)
        recalculate = (days + holidays)
        if increment:
            date = date_start + timedelta(days=recalculate)
        else:
            date = date_start - timedelta(days=recalculate)
        date = self.correct_days_to_workable(date, increment)
        return date

    def on_change_dates(self, date_start, date_end, vals):
        vals['estimated_days'] = self.count_days_without_weekend(
            fields.Datetime.from_string(date_start),
            fields.Datetime.from_string(date_end))
        calculation_type = self.project_id.calculation_type
        if calculation_type:
            date_start = (self.project_id.date_start
                          if calculation_type == 'date_begin'
                          else date_end)
            date_end = (date_start
                        if calculation_type == 'date_begin'
                        else self.project_id.date)
            vals['from_days'] = self.count_days_without_weekend(
                fields.Datetime.from_string(date_start),
                fields.Datetime.from_string(date_end))
        return vals

    @api.multi
    def write(self, vals):
        date_start = (vals.get('date_start')
                      if vals.get('date_start') else self.date_start)
        date_end = (vals.get('date_end')
                    if vals.get('date_end') else self.date_end)
        if date_start and date_end:
            vals = self.on_change_dates(date_start, date_end, vals)
        return super(ProjectTask, self).write(vals)

    def task_recalculate(self):
        self.ensure_one()
        increment = (True if self.project_id.calculation_type == 'date_begin'
                     else False)
        project_date = (fields.Datetime.from_string(self.project_id.date_start)
                        if self.project_id.calculation_type == 'date_begin'
                        else fields.Datetime.from_string(self.project_id.date))
        total_days = (self.from_days
                      if increment else self.from_days + self.estimated_days)
        date_start = self.calculate_date_without_weekend(
            project_date, total_days, increment=increment)
        task_date_start = fields.Datetime.to_string(date_start)
        task_date_end = fields.Datetime.to_string(
            self.calculate_date_without_weekend(
                date_start, self.estimated_days))
        self.write({'date_start': task_date_start, 'date_end': task_date_end})
