# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
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
from openerp import api, models, fields, _


class newsletter_type(models.Model):
    _name = 'newsletter.type'
    _description = 'Newsletter type'

    name = fields.Char('Name', required=True)
    email_template_id = fields.Many2one(
        'email.template', 'Email template', required=True)
    model = fields.Many2one('ir.model', 'Model', required=True)
    domain = fields.Char('Domain', required=True)
    email_from = fields.Char('From address', required=True)
    group_ids = fields.Many2many(
        'res.groups', relation='newsletter_type_groups_rel',
        column1='newsletter_id', column2='group_id', string='Groups',
        help='The groups that may send this type of newsletter. '
        'Leave empty for all members of group Newsletter / Senders')

    @api.multi
    def action_show_recipient_objects(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': self.model.model,
            'domain': self.domain,
            'name': _('Recipients'),
        }
