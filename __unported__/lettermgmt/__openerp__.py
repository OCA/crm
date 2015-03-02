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

{
    'name': 'Letter Management',
    'version': '0.1',
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Social Network',
    'summary': 'Track letters, parcels, registered documents',
    'description': """
Letter Management
=================

Using this module you can track Incoming / Outgoing letters, parcels, registered documents
or any other paper documents that are important for company to keep track of.

Contributors
------------
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Parthiv Patel, Tech Receptives (Original 6.0 Author)

""",
    'depends': ['mail'],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        "res_letter_view.xml",
        "letter_folder_view.xml",
        "letter_channel_view.xml",
        "letter_class_view.xml",
        "letter_history_view.xml",
        "letter_reassignment_view.xml",
        "letter_type_view.xml",
        "letter_sequence.xml",
        'security/ir.model.access.csv',
    ],
    'demo': ["letter_demo.xml"],
    'test': [],
    'installable': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
