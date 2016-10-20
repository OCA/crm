# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class LetterReassignmentLine(models.Model):
    """A line to forward a letter with a comment"""
    _name = 'letter.reassignment'
    _description = 'Reassignment line'

    name = fields.Many2one('res.users', help='User to forward letter to.')
    comment = fields.Text(help='Comment for user explaining forward.')
    letter_id = fields.Many2one(
        'res.letter', string='Letter',
        help='Letter in question.')
