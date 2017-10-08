# -*- coding: utf-8 -*-
# Copyright Savoir-faire Linux, Equitania Software GmbH, Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.one
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
