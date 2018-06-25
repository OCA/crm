# -*- coding: utf-8 -*-
# Copyright Savoir-faire Linux, Equitania Software GmbH, Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class CrmAction(models.Model):
    _name = 'crm.action'
    _description = 'CRM Action'
    _order = 'date desc'

    lead_id = fields.Many2one('crm.lead', string='Lead', ondelete='cascade')

    @api.onchange('lead_id')
    def check_change(self):
        lead = self.lead_id
        if lead and lead.partner_id:
            self.partner_id = lead.partner_id.id

    partner_id = fields.Many2one('res.partner', string='Customer')
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)

    def search_action_types(self):
        return self.env['crm.action.type'].search([('is_active', '=', True)], order='priority')

    def default_action_type(self):
        action_types = self.search_action_types()
        return action_types and action_types[0].id or False

    action_type = fields.Many2one('crm.action.type', string='Type', required=True, default=default_action_type)
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
