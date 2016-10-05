# -*- encoding: utf-8 -*-
#    Hardikgiri Goswami <hardikgiri.goswami@gmail.com>
#    Parthiv Pate, Tech Receptives, Open Source For Ideas
#    Copyright (C) 2009-Today Tech Receptives(http://techreceptives.com).
#    Copyright (C) 2015 Therp BV <http://therp.nl>.
#    All Rights Reserved

from openerp import models, fields, api


class ResLetter(models.Model):
    """A register class to log all movements regarding letters"""
    _name = 'res.letter'
    _description = "Log of Letter Movements"
    _inherit = 'mail.thread'

    @api.model
    def create(self, vals):
        if ('number' not in vals) or (vals.get('number') in ('/', False)):
            sequence = self.env['ir.sequence']
            move_type = vals.get('move', self.env.context.get(
                'default_move', self.env.context.get('move', 'in')))
            vals['number'] = sequence.next_by_code('%s.letter' % move_type)
        return super(ResLetter, self).create(vals)

    def default_recipient(self):
        move_type = self.env.context.get('move', False)
        if move_type == 'in':
            return self.env.user.company_id.partner_id

    def default_sender(self):
        move_type = self.env.context.get('move', False)
        if move_type == 'out':
            return self.env.user.company_id.partner_id

    name = fields.Text('Subject', help="Subject of letter.")
    folder_id = fields.Many2one(
        'letter.folder', string='Folder',
        help='Folder which contains letter.')
    number = fields.Char(
        'Number', help="Auto Generated Number of letter.",
        default="/", required=True)
    move = fields.Selection(
        [('in', 'IN'), ('out', 'OUT')], 'Move', readonly=True,
        help="Incoming or Outgoing Letter.",
        default=lambda self: self.env.context.get('move', 'in'))
    type_id = fields.Many2one(
        'letter.type', string='Type',
        help="Type of Letter, Depending upon size.")
    category_ids = fields.Many2many(
        'letter.category', string='Tags', help="Classification of Document.")
    date = fields.Datetime('Letter Date', help='The letter\'s date')
    snd_date = fields.Datetime(
        'Sent / Received Date', defalut=fields.datetime.now,
        help='Created Date of Letter Logging.')
    rcv_date = fields.Datetime(
        'Sent / Received Date', defalut=fields.datetime.now,
        help='Created Date of Letter Logging.')
    recipient_partner_id = fields.Many2one(
        'res.partner', string='Recipient', track_visibility='onchange',
        default=default_recipient)
    sender_partner_id = fields.Many2one(
        'res.partner', string='Sender', track_visibility='onchange',
        default=default_sender)
    note = fields.Text('Note')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rec', 'Received'),
        ('sent', 'Sent'),
        ('rec_bad', 'Received Damage'),
        ('rec_ret', 'Received But Returned'),
        ('cancel', 'Cancelled')],
        'State', readonly=True, default="draft", track_visibility='onchange')
    parent_id = fields.Many2one('res.letter', 'Parent')
    child_line = fields.One2many(
        'res.letter', 'parent_id', 'Letter Lines')
    channel_id = fields.Many2one(
        'letter.channel', 'Sent / Receive Source')
    orig_ref = fields.Char(
        'Original Reference', help="Reference Number at Origin.")
    expeditor_ref = fields.Char(
        'Expeditor Reference', help="Reference Number used by Expeditor.")
    track_ref = fields.Char(
        'Tracking Reference', help="Reference Number used for Tracking.")
    weight = fields.Float('Weight (in KG)')
    size = fields.Char('Size')
    reassignment_ids = fields.One2many(
        'letter.reassignment', 'letter_id', string='Reassignment lines',
        help='Reassignment users and comments')
    extern_partner_ids = fields.Many2many(
        'res.partner', string='Recipients')

    @api.multi
    def action_received(self):
        """Put the state of the letter into Received"""
        for rec in self:
            rec.write({
                'state': 'rec',
                'rcv_date': self.rcv_date or fields.Date.today()
            })
        return True

    @api.multi
    def action_cancel(self):
        """Put the state of the letter into Cancelled"""
        self.write({'state': 'cancel'})
        return True

    @api.multi
    def action_cancel_draft(self):
        """ Go from cancelled state to draf state """
        self.write({'state': 'draft'})
        return True

    @api.multi
    def action_send(self):
        """Put the state of the letter into sent"""
        for rec in self:
            self.write({
                'state': 'sent',
                'snd_date': rec.snd_date or
                fields.datetime.now()
            })
        return True

    @api.multi
    def action_rec_ret(self):
        """Put the state of the letter into Received but Damaged"""
        for rec in self:
            rec.write({
                'state': 'rec_ret',
                'rcv_date': self.rcv_date or fields.Date.today()
            })
        return True

    @api.multi
    def action_rec_bad(self):
        """Put the state of the letter into Received but Damaged"""
        for rec in self:
            rec.write({
                'state': 'rec_bad',
                'rcv_date': self.rcv_date or fields.Date.today()
            })
        return True
