# -*- coding: utf-8 -*-
# © 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def count_actions(self):
        self.actions_count = len(self.action_ids)

    @api.multi
    @api.depends(
        'action_ids.date', 'action_ids.display_name', 'action_ids.state')
    def compute_next_action(self):
        for lead in self:
            actions = self.env['crm.action'].search(
                [('lead_id', '=', lead.id), ('state', '=', 'draft')],
                order='date', limit=1)
            if actions:
                lead.next_action_id = actions[0]
            else:
                lead.next_action_id = False

    @api.multi
    def next_action_done(self):
        self.ensure_one()
        lead = self[0]
        if lead.next_action_id:
            lead.next_action_id.button_confirm()
        return True

    actions_count = fields.Integer(compute='count_actions')
    action_ids = fields.One2many(
        'crm.action', 'lead_id', string='Actions')
    # replace native fields "date_action" (Next Action Date)
    # and "title_action" (Next Action) by related fields
    date_action = fields.Date(
        related='next_action_id.date', readonly=True, store=True)
    title_action = fields.Char(
        related='next_action_id.display_name', store=True, readonly=True)
    next_action_id = fields.Many2one(
        'crm.action', string='Next Action',
        compute='compute_next_action', readonly=True, store=True)
