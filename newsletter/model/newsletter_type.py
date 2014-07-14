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

from openerp.osv.orm import Model
from openerp.osv import fields


class newsletter_type(Model):
    _name = 'newsletter.type'

    _plaintext_mode_selection = [
        ('manual', 'manual'),
        ('from_html', 'from HTML')
    ]

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'email_template_id': fields.many2one(
            'email.template', 'Email template', required=True),
        'model': fields.many2one('ir.model', 'Model', required=True),
        'domain': fields.char('Domain', size=256, required=True),
        'email_from': fields.char('From address', size=128, required=True),
        'plaintext_mode': fields.selection(
            _plaintext_mode_selection, 'Plaintext mode', required=True),
        'group_ids': fields.many2many(
            'res.groups',
            'newsletter_type_groups_rel', 'newsletter_id', 'group_id',
            'Groups',
            help='The groups that may send this type of newsletter. '
            'Leave empty for all members of group Newsletter / Senders'),
    }

    _defaults = {
        'plaintext_mode': 'from_html',
    }

    def action_show_recipient_objects(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'view_type': 'form',
                'res_model': this.model.model,
                'domain': this.domain,
            }
