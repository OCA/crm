# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class LetterType(models.Model):
    """Class to define various types for letters like : envelope,parcel,
    etc."""
    _name = 'letter.type'
    _description = "Letter Type"

    name = fields.Char(required=True)
    code = fields.Char(required=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique !')
    ]
