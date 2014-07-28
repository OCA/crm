# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.tools.translate import _


class ResPartner(Model):
    _inherit = 'res.partner'

    _columns = {
        'newsletter_ids': fields.many2many(
            'newsletter_newsletter',
            'newsletter_partner_rel', 'partner_id', 'newsletter_id',
            string='Newsletter'),
    }

    def button_show_newsletters(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Received newsletters'),
            'res_model': 'newsletter.newsletter',
            'view_type': 'form',
            'views': [(False, 'tree'), (False, 'form')],
            'domain': [('partner_ids', 'in', ids)],
        }
