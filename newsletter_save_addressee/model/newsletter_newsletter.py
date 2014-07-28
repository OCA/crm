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


class NewsletterNewsletter(Model):
    _inherit = 'newsletter.newsletter'

    _columns = {
        'partner_ids': fields.many2many(
            'res.partner',
            'newsletter_partner_rel', 'newsletter_id', 'partner_id',
            string='Partners'),
        'type_model': fields.related(
            'type_id', 'model', 'model', type='char', string='Model'),
    }

    def _do_send_newsletter(self, cr, uid, this, record_id, context=None):
        result = super(NewsletterNewsletter, self)._do_send_newsletter(
            cr, uid, this, record_id, context=None)
        if this.type_id.model.model == 'res.partner':
            self.pool['newsletter.partner.rel'].create(
                cr, uid,
                {
                    'partner_id': record_id,
                    'newsletter_id': this.id,
                },
                context=context)
        return result

    def button_show_partners(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Recipients'),
            'res_model': 'res.partner',
            'view_type': 'form',
            'views': [(False, 'tree'), (False, 'form')],
            'domain': [('newsletter_ids', 'in', ids)],
        }
