# -*- coding: utf-8 -*-
# Copyright (C) 2009-Today Tech Receptives(http://techreceptives.com).
# Parthiv Pate, Tech Receptives, Open Source For Ideas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class LetterChannel(models.Model):
    """ Class to define various channels using which letters can be sent or
    received like : post, fax, email. """
    _name = 'letter.channel'
    _description = "Send/Receive channel"

    name = fields.Char('Type', required=True)
