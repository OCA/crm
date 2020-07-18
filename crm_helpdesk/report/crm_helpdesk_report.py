# Copyright 2004-2010 Tiny SPRL (<http://tiny.be>)
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.sql import drop_view_if_exists


AVAILABLE_STATES = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('cancel', 'Cancelled'),
    ('done', 'Closed'),
    ('pending', 'Pending')
]


class CrmHelpdeskReport(models.Model):
    """ Helpdesk report after Sales Services """

    _name = "crm.helpdesk.report"
    _description = "Helpdesk report after Sales Services"
    _auto = False

    date = fields.Datetime('Date', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    team_id = fields.Many2one('crm.team', string='Team', readonly=True)
    nbr_requests = fields.Integer('# of Requests', readonly=True)
    state = fields.Selection(AVAILABLE_STATES, string='Status', readonly=True)
    delay_close = fields.Float('Delay to Close', digits=(16, 2),
                               readonly=True, group_operator="avg")
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 readonly=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 readonly=True)
    date_deadline = fields.Date('Deadline', index=True)
    priority = fields.Selection([('5', 'Lowest'), ('4', 'Low'),
                                 ('3', 'Normal'), ('2', 'High'),
                                 ('1', 'Highest')], 'Priority')
    channel_id = fields.Many2one('utm.medium', string='Channel')
    tag_ids = fields.Many2one('crm.lead.tag', string='Tags',
                              domain="[('team_id','=',team_id)]")
    create_date = fields.Datetime('Creation Date', readonly=True, index=True)
    date_closed = fields.Datetime('Close Date', readonly=True, index=True)
    delay_expected = fields.Float('Overpassed Deadline', digits=(16, 2),
                                  readonly=True, group_operator="avg")
    email = fields.Integer('# Emails', size=128, readonly=True)

    @api.model_cr
    def init(self):
        """
            Display Deadline, Responsible user, Partner, Department
        """

        drop_view_if_exists(self._cr, 'crm_helpdesk_report')
        self._cr.execute("""
            create or replace view crm_helpdesk_report as (
                select
                    min(c.id) as id,
                    c.date as date,
                    c.create_date,
                    c.date_closed,
                    c.state,
                    c.user_id,
                    c.team_id,
                    c.partner_id,
                    c.company_id,
                    c.priority,
                    c.date_deadline,
                    c.tag_ids,
                    c.channel_id,
                    count(*) as nbr_requests,
                    extract('epoch' from (c.date_closed-c.create_date)
                        )/(3600*24) as  delay_close,
                    (SELECT count(id)
                     FROM mail_message
                     WHERE model='crm.helpdesk'
                        AND res_id=c.id
                        AND message_type = 'email') AS email,
                    abs(avg(
                        extract('epoch' from (c.date_deadline - c.date_closed)
                            ))/(3600*24)) as delay_expected
                from
                    crm_helpdesk c
                where c.active = 'true'
                group by c.date,c.state,c.user_id,c.team_id,c.priority,
                     c.partner_id,c.company_id,c.date_deadline,c.create_date,
                     c.date,c.date_closed,c.tag_ids,c.channel_id,c.id
            )""")
