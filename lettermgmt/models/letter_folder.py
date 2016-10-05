# -*- coding: utf-8 -*-
# copyright (C) 2013 Savoir-faire Linux <http://www.savoirfairelinux.com>
# Hardikgiri Goswami <hardikgiri.goswami@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class LetterFolder(models.Model):
    """Folder which contains collections of letters"""
    _name = 'letter.folder'
    _description = 'Letter Folder'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    letter_ids = fields.One2many(
        'res.letter', 'folder_id', string='Letters',
        help='Letters contained in this folder.')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique !')
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
