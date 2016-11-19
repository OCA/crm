# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class LetterChannel(models.Model):
    """ Class to define various channels using which letters can be sent or
    received like : post, fax, email. """
    _name = 'letter.channel'
    _description = "Send/Receive channel"

    name = fields.Char(required=True)
