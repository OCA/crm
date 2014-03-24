# -*- encoding: utf-8 -*-
##############################################################################
#
#    Parthiv Pate, Tech Receptives, Open Source For Ideas
#    Copyright (C) 2009-Today Tech Receptives(http://techreceptives.com).
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
from openerp.tools.translate import _


class letter_type(orm.Model):
    """Class to define various types for letters like : envelope,parcel, etc."""
    _name = 'letter.type'
    _description = _("Letter Type")
    _columns = {
        'name': fields.char('Type', size=32, required=True),
        'code': fields.char('Code', size=8, required=True),
    }
    _sql_constraints = [('code_uniq', 'unique(code)', 'Code must be unique !')]
