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

from openerp import models
from datetime import datetime, timedelta


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def reorganize_project(self, event, date_begin=None):
        project_task_obj = self.env['project.task']
        self.write({'name': event.name})
        obj_ids = project_task_obj.search([('project_id', '=', self.id)])
        for obj_id in obj_ids:
            project_task = project_task_obj.browse(int(obj_id))
            if date_begin:
                if type(date_begin) is str:
                    date_begin = datetime.strptime(
                        date_begin, "%Y-%m-%d %H:%M:%S")
            else:
                date_begin = datetime.strptime(
                    event.date_begin, "%Y-%m-%d %H:%M:%S")

            if project_task.previous_day > 0:
                pdays = int(project_task.previous_day) * -1
                date_start = (date_begin + timedelta(days=pdays)).strftime(
                    "%Y-%m-%d %H:%M:%S")
                project_task.write({'date_start': str(date_start)})
            else:
                date_start = (date_begin).strftime(
                    "%Y-%m-%d %H:%M:%S")
                project_task.write({'date_start': str(date_start)})
