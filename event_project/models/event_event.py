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

from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_template = fields.Many2one(
        comodel_name='project.project', string='Template project',
        domain="[('state', '=', 'template')]")
    project = fields.Many2one(
        comodel_name='project.project', string='Related project',
        readonly=True)

    def get_project_with_duplicate_template(self, template):
        project_obj = self.env['project.project']
        result = template.duplicate_template()
        return project_obj.browse(int(result['res_id']))

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        if (event.project_template and not event.project):
            event.project = self.get_project_with_duplicate_template(
                event.project_template)
            event.project.reorganize_project(event, name=vals.get('name'))
        return event

    @api.one
    def write(self, vals):
        project_obj = self.env['project.project']
        project = None
        date_begin = None
        if vals.get('project_template') and not self.project:
                project_template = project_obj.browse(
                    int(vals['project_template']))
                project = self.get_project_with_duplicate_template(
                    project_template)
                vals['project'] = project.id
        else:
            project = self.project
        date_begin = fields.Datetime.from_string(
            self.date_begin) if not vals.get(
            'date_begin') else fields.Datetime.from_string(vals['date_begin'])
        if date_begin:
            project.reorganize_project(
                self, date_begin=date_begin, name=vals.get('name'))
        return super(EventEvent, self).write(vals)
