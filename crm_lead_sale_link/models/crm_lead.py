# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from openerp import models, fields, api, _


sales_order_states = [
    'progress', 'manual', 'shipping_exept', 'invoice_except', 'done']

quotations_states = ['draft', 'sent', 'waiting_date']


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def count_sales_order(self):
        if not self.partner_id:
            return False
        self.sales_order_count = self.env['sale.order'].search_count([
            ('partner_id', '=', self.partner_id.id),
            ('state', 'in', sales_order_states),
        ])
        self.quotations_count = self.env['sale.order'].search_count([
            ('partner_id', '=', self.partner_id.id),
            ('state', 'in', quotations_states),
        ])

    sales_order_count = fields.Integer(compute='count_sales_order')
    quotations_count = fields.Integer(compute='count_sales_order')

    @api.multi
    def get_sale_order_view(self, order_states, view_title):
        partner_ids = [lead.partner_id.id for lead in self]

        orders = self.env['sale.order'].search([
            ('partner_id', 'in', partner_ids),
            ('state', 'in', order_states),
        ])

        res = {
            'name': view_title,
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
        }

        if len(orders) == 1:
            res['res_id'] = orders[0].id
            res['view_mode'] = 'form'
        else:
            res['domain'] = [
                ('state', 'in', order_states),
                ('partner_id', 'in', partner_ids),
            ]
            res['view_mode'] = 'tree,form'

        return res

    @api.multi
    def button_sales_orders(self):
        return self.get_sale_order_view(sales_order_states, _('Sales Order'))

    @api.multi
    def button_quotations(self):
        return self.get_sale_order_view(quotations_states, _('Quotations'))
