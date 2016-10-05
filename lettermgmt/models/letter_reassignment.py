# -*- coding: utf-8 -*-
# copyright (C) 2013 Savoir-faire Linux <http://www.savoirfairelinux.com>
# Hardikgiri Goswami <hardikgiri.goswami@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class LetterReassignment(models.Model):
    """A line to forward a letter with a comment"""
    _name = 'letter.reassignment'
    _description = 'Reassignment line'

    name = fields.Many2one(
        'res.users', string='Name', help='User to forward letter to.')
    comment = fields.Text(
        'Comment', help='Comment for user explaining forward.')
    letter_id = fields.Many2one(
        'res.letter', string='Letter', help='Letter in question.')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
