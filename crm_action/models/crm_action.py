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

from openerp import models, fields, api


class CrmAction(models.Model):
    _name = 'crm.action'
    _description = 'CRM Action'

    lead_id = fields.Many2one(
        'crm.lead', string='Lead', ondelete='cascade')

    @api.onchange('lead_id')
    def check_change(self):
        lead = self.lead_id
        if lead and lead.partner_id:
            self.partner_id = lead.partner_id.id

    partner_id = fields.Many2one(
        'res.partner', string='Customer')

    date = fields.Date(
        'Date', required=True,
        default=fields.Date.context_today)

    user_id = fields.Many2one(
        'res.users', string='User', required=True,
        default=lambda self: self.env.user)

    def search_action_types(self):
        return self.env['crm.action.type'].search(
            [('is_active', '=', True)], order='priority')

    def default_action_type(self):
        action_types = self.search_action_types()
        return action_types and action_types[0].id or False

    action_type = fields.Many2one(
        'crm.action.type', string='Type', required=True,
        default=default_action_type)

    details = fields.Text('Details')

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('done', 'Done'),
        ], string='Status', required=True,
        default="draft")

    @api.multi
    def button_confirm(self):
        self.write({'state': 'done'})

    @api.multi
    def button_set_to_draft(self):
        self.write({'state': 'draft'})
