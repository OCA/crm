# -*- coding: utf-8 -*-
# Copyright 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def compute_count_actions(self):
        self.actions_count = len(self.action_ids)

    actions_count = fields.Integer(
        compute='compute_count_actions',
    )
    action_ids = fields.One2many(
        comodel_name='crm.action',
        inverse_name='lead_id',
        string='Actions',
    )
    # replace native fields "date_action" (Next Action Date)
    # and "title_action" (Next Action) by related fields
    date_action = fields.Date(
        related='next_action_id.date',
        readonly=True,
        store=True,
    )
    title_action = fields.Char(
        related='next_action_id.display_name',
        readonly=True,
        store=True,
    )
    next_action_id = fields.Many2one(
        comodel_name='crm.action',
        string='Next Action',
        compute='compute_next_action',
        readonly=True, store=True,
    )

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
        if self.next_action_id:
            self.next_action_id.button_confirm()
        return True
