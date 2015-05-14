# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Javier Iniesta <javieria@antiun.com>
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

from openerp import models, fields
from datetime import timedelta


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def reorganize_project(self, event, date_begin=None, name=None):
        project_task_obj = self.env['project.task']
        project_task_type_done = self.env.ref('project.project_tt_deployment')
        project_task_ids = project_task_obj.search(
            [('project_id', '=', self.id),
             ('stage_id', '!=', project_task_type_done.id)])
        if not date_begin:
            date_begin = fields.Datetime.from_string(event.date_begin)
        max_anticipation_days = 0
        for project_task in project_task_ids:
            date_start = fields.Datetime.to_string(
                date_begin - timedelta(
                    days=int(project_task.anticipation_days)))
            project_task.write({'date_start': str(date_start)})
            if max_anticipation_days < int(project_task.anticipation_days):
                max_anticipation_days = int(project_task.anticipation_days)
        first_date_start = fields.Datetime.to_string(
            date_begin - timedelta(
                days=int(max_anticipation_days)))

        vals = {'date': date_begin,
                'date_start': first_date_start}
        if name:
            vals['name'] = name
        self.write(vals)
