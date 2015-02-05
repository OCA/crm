# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
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
##############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from newsletter_type import newsletter_type
from newsletter_newsletter import _get_plaintext


class newsletter_topic(Model):
    _name = 'newsletter.topic'

    _columns = {
        'newsletter_id': fields.many2one(
            'newsletter.newsletter', 'Newsletter'),
        'title': fields.char('Title', size=256),
        'text_plain': fields.function(
            _get_plaintext, type='text', string='Text (plain)',
            arg='text_html', store=True),
        'text_html': fields.text('Text (html)'),
    }
