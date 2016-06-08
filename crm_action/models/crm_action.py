# -*- coding: utf-8 -*-
# © 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class CrmAction(models.Model):
    _name = 'crm.action'
    _description = 'CRM Action'
    _order = 'date'
    _rec_name = 'display_name'

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
        return self.env['crm.action.type'].search([], order='priority')

    def default_action_type(self):
        action_types = self.search_action_types()
        return action_types and action_types[0].id or False

    action_type_id = fields.Many2one(
        'crm.action.type', string='Type', required=True,
        default=default_action_type)

    details = fields.Text('Details')

    state = fields.Selection(
        [
            ('draft', 'Todo'),
            ('done', 'Done'),
        ], string='Status', required=True, readonly=True,
        default="draft")

    @api.multi
    @api.depends('action_type_id.name', 'details')
    def compute_display_name(self):
        for action in self:
            if action.details:
                action.display_name = u'[%s] %s' % (
                    action.action_type_id.name, action.details)
            else:
                action.display_name = u'[%s]' % action.action_type_id.name

    display_name = fields.Char(
        compute='compute_display_name', readonly=True, store=True)

    @api.multi
    def button_confirm(self):
        self.write({'state': 'done'})

    @api.multi
    def button_set_to_draft(self):
        self.write({'state': 'draft'})
