# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class LetterFolder(models.Model):
    """Folder which contains collections of letters"""
    _name = 'letter.folder'
    _description = 'Letter Folder'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    letter_ids = fields.One2many(
        'res.letter', 'folder_id', string='Letters',
        help='Letters contained in this folder.')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique !')
    ]
