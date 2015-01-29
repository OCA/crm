# -*- encoding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from openerp.osv import fields, orm


class letter_reassignment(orm.Model):
    """A line to forward a letter with a comment"""
    _name = 'letter.reassignment'
    _description = 'Reassignment line'
    _columns = {
        'name': fields.many2one(
            'res.users', string='Name', help='User to forward letter to.'),
        'comment': fields.text(
            'Comment', help='Comment for user explaining forward.'),
        'letter_id': fields.many2one(
            'res.letter', string='Letter', help='Letter in question.'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
