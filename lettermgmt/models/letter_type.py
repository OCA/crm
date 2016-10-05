# -*- encoding: utf-8 -*-
# Copyright (C) 2009-Today Tech Receptives(http://techreceptives.com).
# Parthiv Pate, Tech Receptives, Open Source For Ideas
# Hardikgiri Goswami <hardikgiri.goswami@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class LetterType(models.Model):
    """Class to define various types for letters like : envelope,parcel,
    etc."""
    _name = 'letter.type'
    _description = "Letter Type"

    name = fields.Char('Type', required=True)
    code = fields.Char('Code', required=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique !')
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
