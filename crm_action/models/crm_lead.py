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


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def count_actions(self):
        self.actions_count = len(self.action_ids)

    actions_count = fields.Integer(compute='count_actions')
    action_ids = fields.One2many(
        'crm.action', 'lead_id', string='Actions')

    @api.multi
    def button_actions(self):
        self.ensure_one()

        res = {
            'name': _('Actions'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.action',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('lead_id', '=', self[0].id)],
        }

        return res
