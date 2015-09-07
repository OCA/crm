# -*- encoding: utf-8 -*-
##############################################################################
#
#    Parthiv Pate, Tech Receptives, Open Source For Ideas
#    Copyright (C) 2009-Today Tech Receptives(http://techreceptives.com).
#    Copyright (C) 2015 Therp BV <http://therp.nl>.
#    All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp.osv import fields, orm


class res_letter(orm.Model):
    """A register class to log all movements regarding letters"""
    _name = 'res.letter'
    _description = "Log of Letter Movements"
    _inherit = 'mail.thread'

    def _get_number(self, cr, uid, context=None):
        if context is None:
            context = {}
        sequence_pool = self.pool.get('ir.sequence')
        move_type = context.get('move', 'in')
        return sequence_pool.get(
            cr, uid, '%s.letter' % move_type, context=context)

    _columns = {
        'name': fields.text('Subject', help="Subject of letter."),
        'folder_id': fields.many2one(
            'letter.folder', string='Folder',
            help='Folder which contains letter.'),
        'number': fields.char(
            'Number', help="Auto Generated Number of letter.",
            required=True),
        'move': fields.selection(
            [('in', 'IN'), ('out', 'OUT')], 'Move', readonly=True,
            help="Incoming or Outgoing Letter."),
        'type': fields.many2one(
            'letter.type', 'Type',
            help="Type of Letter, Depending upon size."),
        'class': fields.many2one(
            'letter.class', 'Class', help="Classification of Document."),
        'date': fields.datetime('Letter Date', help='The letter\'s date'),
        'snd_rec_date': fields.datetime(
            'Sent / Received Date', help='Created Date of Letter Logging.'),
        'recipient_partner_id': fields.many2one(
            'res.partner', string='Recipient', track_visibility='onchange'),
        'sender_partner_id': fields.many2one(
            'res.partner', string='Sender', track_visibility='onchange'),
        'note': fields.text('Note'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('created', 'Created'),
                                   ('validated', 'Validated'),
                                   ('rec', 'Received'),
                                   ('sent', 'Sent'),
                                   ('rec_bad', 'Received Damage'),
                                   ('rec_ret', 'Received But Returned'),
                                   ('cancel', 'Cancelled')],
                                  'State', readonly=True,
                                  track_visibility='onchange'),
        'parent_id': fields.many2one('res.letter', 'Parent'),
        'child_line': fields.one2many(
            'res.letter', 'parent_id', 'Letter Lines'),
        'channel_id': fields.many2one(
            'letter.channel', 'Sent / Receive Source'),
        'orig_ref': fields.char(
            'Original Reference', help="Reference Number at Origin."),
        'expeditor_ref': fields.char(
            'Expeditor Reference', help="Reference Number used by Expeditor."),
        'track_ref': fields.char(
            'Tracking Reference', help="Reference Number used for Tracking."),
        'weight': fields.float('Weight (in KG)'),
        'size': fields.char('Size'),
        'reassignment_ids': fields.one2many(
            'letter.reassignment', 'letter_id', string='Reassignment lines',
            help='Reassignment users and comments'),
        'extern_partner_ids': fields.many2many(
            'res.partner', string='Recipients'),
    }

    _defaults = {
        'number': _get_number,
        'snd_rec_date': fields.datetime.now,
        'move': lambda self, cr, uid, context: context.get('move', 'in'),
        'state': 'draft',
    }

    def action_received(self, cr, uid, ids, context=None):
        """Put the state of the letter into Received"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [letter.id], {'state': 'rec'}, context=context)
            if letter.recipient_partner_id:
                letter.message_subscribe([letter.recipient_partner_id.id])
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        """Put the state of the letter into Cancelled"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id], {'state': 'cancel'}, context=context)
        return True

    def action_create(self, cr, uid, ids, context=None):
        """Put the state of the letter into Crated"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id], {'state': 'created'}, context=context)
        return True

    def action_validate(self, cr, uid, ids, context=None):
        """Put the state of the letter into Validated"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id], {'state': 'validated'}, context=context)
        return True

    def action_send(self, cr, uid, ids, context=None):
        """Put the state of the letter into sent"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id],
                {
                    'state': 'sent',
                    'snd_rec_date': letter.snd_rec_date or
                    fields.datetime.now()
                },
                context=context)
            if letter.sender_partner_id:
                letter.message_subscribe([letter.sender_partner_id.id])
        return True

    def action_rec_ret(self, cr, uid, ids, context=None):
        """Put the state of the letter into Received but Returned"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id], {'state': 'rec_ret'}, context=context)
        return True

    def action_rec_bad(self, cr, uid, ids, context=None):
        """Put the state of the letter into Received but Damaged"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id], {'state': 'rec_bad'}, context=context)
        return True

    def action_set_draft(self, cr, uid, ids, context=None):
        """Put the state of the letter into draft"""
        for letter in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [letter.id], {'state': 'draft'}, context=context)
        return True
