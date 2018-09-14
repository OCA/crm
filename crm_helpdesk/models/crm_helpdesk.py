# Copyright 2004-2010 Tiny SPRL (<http://tiny.be>)
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.tools.mail import html2plaintext


class CrmHelpdesk(models.Model):
    """ Helpdesk Cases """

    _name = "crm.helpdesk"
    _description = "Helpdesk"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, index=True,)
    active = fields.Boolean('Active', required=False, default=True)
    date_action_last = fields.Datetime('Last Action', readonly=1)
    date_action_next = fields.Datetime('Next Action', readonly=1)
    description = fields.Text('Description')
    create_date = fields.Datetime('Creation Date', readonly=True)
    write_date = fields.Datetime('Update Date', readonly=True)
    date_deadline = fields.Date('Deadline')
    user_id = fields.Many2one(
        'res.users', string='Responsible', index=True,
        default=lambda self: self.env.user)
    team_id = fields.Many2one(
        'crm.team', string='Sales Team', index=True,
        help='Responsible sales team. Define Responsible user and '
             'Email account for mail gateway.')
    company_id = fields.Many2one(
        'res.company', string='Company', index=True,
        default=lambda self: self.env.user.company_id.id)
    date_open = fields.Datetime('Open', readonly=True)
    date_closed = fields.Datetime('Closed', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True)
    email_cc = fields.Text('Watchers Emails', size=252,
                           help="These email addresses will be added to the "
                                "CC field of all inbound and outbound emails"
                                " for this record before being sent. Separate"
                                " multiple email addresses with a comma")
    contact_name = fields.Char('Contact Name', size=64)
    email_from = fields.Char('Email', size=128, index=True,
                             help="Destination email for email gateway")
    date = fields.Datetime('Date', index=True,
                           default=fields.Datetime.now)
    channel_id = fields.Many2one('utm.medium', string='Channel',
                                 help="Communication channel.")
    planned_revenue = fields.Float('Planned Revenue')
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')],
                                string='Priority', index=True, default='1')
    probability = fields.Float('Probability (%)')
    tag_ids = fields.Many2one(
        'crm.lead.tag', string='Tags')
    duration = fields.Float('Duration', states={'done': [('readonly', True)]})
    lost_reason = fields.Many2one('crm.lost.reason', 'Lost Reason',
                                  index=True, track_visibility='onchange')
    state = fields.Selection(
        [('draft', 'New'),
         ('open', 'In Progress'),
         ('pending', 'Pending'),
         ('done', 'Closed'),
         ('cancel', 'Cancelled')], 'Status', readonly=True,
        track_visibility='onchange', index=True,
        help='The status is set to \'Draft\', when a case is created.\
              \nIf the case is in progress the status is set to \'Open\'.\
              \nWhen the case is over, the status is set to \'Done\'.\
              \nIf the case needs to be reviewed then the status is set to'
             ' \'Pending\'.', default='draft')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.email_from = self.partner_id.email

    @api.multi
    def write(self, values):
        """ Override to add case management: open/close dates """
        if values.get('state'):
            if values.get('state') in ['draft', 'open'] and not values.get(
                    'date_open'):
                values['date_open'] = fields.Datetime.now()
            elif values.get('state') == 'done' and not values.get(
                    'date_closed'):
                values['date_closed'] = fields.Datetime.now()
        return super(CrmHelpdesk, self).write(values)

    # -------------------------------------------------------
    # Mail gateway
    # -------------------------------------------------------

    @api.model
    def _prepare_message_new_custom_values(self, msg, custom_values=None):
        if custom_values is None:
            custom_values = {}
        desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
            'description': desc,
            'email_from': msg.get('from'),
            'email_cc': msg.get('cc'),
            'user_id': False,
            'partner_id': msg.get('author_id', False),
        }
        defaults.update(custom_values)
        return defaults, msg

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the
            mailgateway through message_process.
            This override updates the document according to the email.
        """
        custom_values, msg = self._prepare_message_new_custom_values(
            msg, custom_values)
        return super(CrmHelpdesk, self).message_new(
            msg, custom_values=custom_values)
