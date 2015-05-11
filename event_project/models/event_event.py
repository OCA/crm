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
    project_related = fields.Many2one(
        comodel_name='project.project', string='Related project',
        readonly=True)

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        if (event.project_template and not event.project_related):
            project_obj = self.env['project.project']
            event.project_template.duplicate_template()
            obj_ids = project_obj.search([])
            event.project_related = obj_ids[len(obj_ids) - 1]
            project = project_obj.browse(int(event.project_related))
            project.reorganize_project(event)
        return event

    @api.one
    def write(self, vals):
        project_obj = self.env['project.project']
        project_template = None
        project_related = None
        date_begin = None

        if ((self.project_template or
                ('project_template' in vals and vals['project_template'])) and
                not self.project_related):

            if 'project_template' in vals and vals['project_template']:
                project_template = project_obj.browse(
                    int(vals['project_template']))
            else:
                project_template = self.project_template
            project_template.duplicate_template()

            obj_ids = project_obj.search([])
            project_related = obj_ids[len(obj_ids) - 1]
            vals['project_related'] = project_related.id
        else:
            project_related = self.project_related

        if 'date_begin' in vals and vals['date_begin']:
            date_begin = vals['date_begin']

        if (date_begin or
                ('project_related' in vals and vals['project_related'])):
            project_related.reorganize_project(self, date_begin=date_begin)

        if 'name' in vals and vals['name'] and project_related:
            project_related.write({'name': vals['name']})

        return super(EventEvent, self).write(vals)
