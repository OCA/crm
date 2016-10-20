# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResLetter(models.Model):
    """A register class to log all movements regarding letters"""
    _name = 'res.letter'
    _description = "Log of Letter Movements"
    _inherit = 'mail.thread'

    number = fields.Char(
        help="Auto Generated Number of letter.",
        default="/")
    name = fields.Text(
        string='Subject',
        help="Subject of letter.")
    move = fields.Selection(
        [('in', 'IN'), ('out', 'OUT')],
        help="Incoming or Outgoing Letter.",
        readonly=True,
        default=lambda self: self.env.context.get('move', 'in'))

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('rec', 'Received'),
            ('rec_bad', 'Received Damage'),
            ('rec_ret', 'Received But Returned'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
        readonly=True,
        copy=False,
        track_visibility='onchange',
        help="""
            * Draft: not confirmed yet.\n
            * Sent: has been sent, can't be modified anymore.\n
            * Received: has arrived.\n
            * Received Damage: has been received with damages.\n
            * Received But Returned: has been received but returned.\n
            * Cancel: has been cancelled, can't be sent anymore."""
        )

    date = fields.Date(
        string='Letter Date',
        help='The letter\'s date.',
        default=fields.Date.today)
    snd_date = fields.Date(
        string='Sent Date',
        help='The date the letter was sent.')
    rec_date = fields.Date(
        string='Received Date',
        help='The date the letter was received.')

    def default_recipient(self):
        move_type = self.env.context.get('move', False)
        if move_type == 'in':
            return self.env.user.company_id.partner_id

    def default_sender(self):
        move_type = self.env.context.get('move', False)
        if move_type == 'out':
            return self.env.user.company_id.partner_id

    recipient_partner_id = fields.Many2one(
        'res.partner',
        string='Recipient',
        track_visibility='onchange',
        # required=True, TODO: make it required in 9.0
        default=default_recipient)
    sender_partner_id = fields.Many2one(
        'res.partner',
        string='Sender',
        track_visibility='onchange',
        # required=True, TODO: make it required in 9.0
        default=default_sender)
    note = fields.Text(
        string='Delivery Notes',
        help='Indications for the delivery officer.')

    channel_id = fields.Many2one(
        'letter.channel',
        string="Channel",
        help='Sent / Receive Source')

    category_ids = fields.Many2many(
        'letter.category',
        string="Tags",
        help="Classification of Document.")

    folder_id = fields.Many2one(
        'letter.folder',
        string='Folder',
        help='Folder which contains letter.')

    type_id = fields.Many2one(
        'letter.type',
        string="Type",
        help="Type of Letter, Depending upon size.")

    weight = fields.Float(help='Weight (in KG)')
    size = fields.Char(help='Size of the package.')

    track_ref = fields.Char(
        string='Tracking Reference',
        help="Reference Number used for Tracking.")
    orig_ref = fields.Char(
        string='Original Reference',
        help="Reference Number at Origin.")
    expeditor_ref = fields.Char(
        string='Expeditor Reference',
        help="Reference Number used by Expeditor.")

    parent_id = fields.Many2one(
        'res.letter',
        string='Parent',
        groups='lettermgmt.group_letter_thread')
    child_line = fields.One2many(
        'res.letter',
        'parent_id',
        string='Letter Lines',
        groups='lettermgmt.group_letter_thread')

    reassignment_ids = fields.One2many(
        'letter.reassignment',
        'letter_id',
        string='Reassignment lines',
        help='Reassignment users and comments',
        groups='lettermgmt.group_letter_reasignment')

    # This field seems to be unused. TODO: Remove it?
    extern_partner_ids = fields.Many2many(
        'res.partner',
        string='Recipients')

    @api.model
    def create(self, vals):
        if ('number' not in vals) or (vals.get('number') in ('/', False)):
            sequence = self.env['ir.sequence']
            move_type = vals.get('move', self.env.context.get(
                'default_move', self.env.context.get('move', 'in')))
            vals['number'] = sequence.get('%s.letter' % move_type)
        return super(ResLetter, self).create(vals)

    @api.one
    def action_cancel(self):
        """ Put the state of the letter into Cancelled """
        self.write({'state': 'cancel'})
        return True

    @api.one
    def action_cancel_draft(self):
        """ Go from cancelled state to draf state """
        self.write({'state': 'draft'})
        return True

    @api.one
    def action_send(self):
        """ Put the state of the letter into sent """
        self.write({
            'state': 'sent',
            'snd_date': self.snd_date or fields.Date.today()
        })
        return True

    @api.one
    def action_received(self):
        """ Put the state of the letter into Received """
        self.write({
            'state': 'rec',
            'rec_date': self.rec_date or fields.Date.today()
        })
        return True

    @api.one
    def action_rec_ret(self):
        """ Put the state of the letter into Received but Returned """
        self.write({
            'state': 'rec_ret',
            'rec_date': self.rec_date or fields.Date.today()
        })
        return True

    @api.one
    def action_rec_bad(self):
        """ Put the state of the letter into Received but Damaged """
        self.write({
            'state': 'rec_bad',
            'rec_date': self.rec_date or fields.Date.today()
        })
        return True
