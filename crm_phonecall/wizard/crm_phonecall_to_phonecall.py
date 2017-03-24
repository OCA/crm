# -*- coding: utf-8 -*-
# Copyright 2004-2010 Tiny SPRL (<http://tiny.be>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models

import time


class CrmPhonecall2phonecall(models.TransientModel):
    _name = 'crm.phonecall2phonecall'
    _description = 'Phonecall To Phonecall'

    name = fields.Char(
        string='Call summary',
        required=True,
        select=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Assign To",
    )
    contact_name = fields.Char(
        string='Contact',
    )
    phone = fields.Char()
    tag_id = fields.Many2one(
        comodel_name='crm.lead.tag',
        string='Tag',
    )
    date = fields.Datetime()
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Sales Team'
    )
    action = fields.Selection(
        selection=[
            ('schedule', 'Schedule a call'),
            ('log', 'Log a call')
        ],
        string='Action',
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
    )
    note = fields.Text()

    @api.multi
    def action_schedule(self):
        phonecall_obj = self.env['crm.phonecall']
        phonecalls = phonecall_obj.browse(self._context.get('active_ids', []))
        for this in self:
            phonecalls.schedule_another_phonecall(
                this.date,
                this.name,
                this.user_id.id,
                this.team_id.id or False,
                this.tag_id.id or False,
                action=this.action,
            )

        return phonecalls.redirect_phonecall_view()

    @api.model
    def default_get(self, fields):
        """
        This function gets default values

        """
        res = super(CrmPhonecall2phonecall, self).default_get(fields)
        res.update({
            'action': 'schedule',
            'date': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        for phonecall in self.env['crm.phonecall'].browse(
                self.env.context.get('active_id')):
            tag_id = False
            data_obj = self.env['ir.model.data']
            try:
                res_id = data_obj._get_id('crm', 'categ_phone2')
                tag_id = data_obj.browse(res_id).res_id
            except ValueError:
                pass
            if 'tag_id' in fields:
                res.update({'tag_id': tag_id})
            for field in ('name', 'user_id.id', 'date', 'team_id.id',
                          'partner_id.id'):
                if field in fields:
                    res[field] = getattr(phonecall, field)
        return res
