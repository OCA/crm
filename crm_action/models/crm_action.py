# -*- coding: utf-8 -*-
# Copyright 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2017 Amaris - Quentin Theuret
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import logging

logger = logging.getLogger(__name__)


class CrmAction(models.Model):
    _name = 'crm.action'
    _description = 'CRM Action'
    _order = 'date'
    _rec_name = 'display_name'

    def default_action_type(self):
        action_types = self.search_action_types()
        return action_types and action_types[0].id or False

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead',
        ondelete='cascade',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'crm.action'),
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )
    date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        required=True,
        default=lambda self: self.env.user,
    )
    action_type_id = fields.Many2one(
        comodel_name='crm.action.type',
        string='Type',
        required=True,
        default=default_action_type,
    )
    details = fields.Text()
    state = fields.Selection(
        selection=[
            ('draft', 'Todo'),
            ('done', 'Done'),
        ],
        string='Status',
        required=True,
        readonly=True,
        default="draft",
    )
    display_name = fields.Char(
        compute='_compute_display_name',
        readonly=True,
        store=True,
    )

    @api.onchange('lead_id')
    def check_change(self):
        lead = self.lead_id
        if lead and lead.partner_id:
            self.partner_id = lead.partner_id
            self.company_id = lead.company_id

    def search_action_types(self):
        return self.env['crm.action.type'].search([], order='priority')

    @api.multi
    def button_confirm(self):
        self.write({'state': 'done'})

    @api.multi
    def button_set_to_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    @api.depends('action_type_id.name', 'details')
    def _compute_display_name(self):
        for action in self:
            if action.details:
                action.display_name = u'[%s] %s' % (
                    action.action_type_id.name, action.details)
            else:
                action.display_name = u'[%s]' % action.action_type_id.name

    @api.model
    def _send_email_reminder(self):
        today = fields.Date.context_today(self)
        actions = self.env['crm.action'].search([
            ('state', '=', 'draft'), ('date', '=', today)])
        logger.info(
            'Preparing CRM actions email reminders '
            '(%d actions found for today)',
            len(actions))
        user_company_actions = {}
        # key = (user, company)
        # value = list of crm.action records
        for action in actions:
            user_company_actions.setdefault(
                (action.user_id, action.company_id), []).append(action)
        mail_template = self.env.ref(
            'crm_action.crm_action_reminder_email_template')
        for (user, company), action_list in user_company_actions.iteritems():
            if user.email:
                mail_template.with_context(
                    crm_action_list=action_list,
                    company=company).send_mail(user.id)
                logger.info(
                    'Sent CRM action email reminder to user %s <%s> '
                    'company %s', user.name, user.email, company.name)
            else:
                logger.warning('Missing email on user %s', user.name)
        return True
