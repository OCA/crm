# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class LetterCategory(models.Model):
    """ Class to define the letter categories like: classified,
    confidential, personal, etc. """
    _name = 'letter.category'
    _description = "Letter Category"

    name = fields.Char(required=True)
