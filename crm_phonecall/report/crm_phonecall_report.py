# -*- coding: utf-8 -*-
# Copyright 2004-2010 Tiny SPRL (<http://tiny.be>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import tools
from openerp import fields, models

AVAILABLE_STATES = [
    ('draft', 'Draft'),
    ('open', 'Todo'),
    ('cancel', 'Cancelled'),
    ('done', 'Held'),
    ('pending', 'Pending')
]


class CrmPhonecallReport(models.Model):
    _name = "crm.phonecall.report"
    _description = "Phone calls by user"
    _auto = False

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        readonly=True,
    )
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Team',
        readonly=True,
    )
    priority = fields.Selection(
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High')
        ],
        string='Priority',
    )
    nbr_cases = fields.Integer(
        string='# of Cases',
        readonly=True,
    )
    state = fields.Selection(
        AVAILABLE_STATES,
        string='Status',
        readonly=True,
    )
    create_date = fields.Datetime(
        string='Create Date',
        readonly=True,
        select=True,
    )
    delay_close = fields.Float(
        string='Delay to close',
        digits=(16, 2),
        readonly=True,
        group_operator="avg",
        help="Number of Days to close the case",
    )
    duration = fields.Float(
        string='Duration',
        digits=(16, 2),
        readonly=True,
        group_operator="avg",
    )
    delay_open = fields.Float(
        string='Delay to open',
        digits=(16, 2),
        readonly=True,
        group_operator="avg",
        help="Number of Days to open the case",
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        readonly=True,
    )
    opening_date = fields.Datetime(
        readonly=True,
        select=True,
    )
    date_closed = fields.Datetime(
        string='Close Date',
        readonly=True,
        select=True)

    def _select(self):
        select_str = """
            select
                id,
                c.date_open as opening_date,
                c.date_closed as date_closed,
                c.state,
                c.user_id,
                c.team_id,
                c.partner_id,
                c.duration,
                c.company_id,
                c.priority,
                1 as nbr_cases,
                c.create_date as create_date,
                extract(
                  'epoch' from (
                  c.date_closed-c.create_date))/(3600*24) as delay_close,
                extract(
                  'epoch' from (
                  c.date_open-c.create_date))/(3600*24) as delay_open
           """
        return select_str

    def _from(self):
        from_str = """
            from crm_phonecall c
        """
        return from_str

    def init(self, cr):

        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            create or replace view %s as (
                %s
                %s
            )""" % (self._table, self._select(), self._from()))
