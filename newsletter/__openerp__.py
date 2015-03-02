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

{
    'name': 'Newsletters',
    'version': '1.0',
    'description': """
    This addon provides the UI and mailing mechanisms for newsletters
    """,
    'author': "Therp BV,Odoo Community Association (OCA)",
    'website': 'http://www.therp.nl',
    "category": "Newsletter",
    "depends": [
        'email_template',
        'web_ckeditor4',
        ],
    'css': [
        ],
    'data': [
        'data/ir_module_cateogry.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/newsletter_type.xml',
        'view/newsletter.xml',
        'view/menu.xml',
        'view/email_template_preview_view.xml',
        'view/newsletter_type.xml',
        ],
    'js': [
        'static/src/js/newsletter.js',
        ],
    'installable': True,
    'active': False,
    'certificate': '',
}
