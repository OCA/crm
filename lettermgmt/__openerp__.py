# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Letter Management',
    'summary': 'Track letters, parcels, registered documents',
    'version': '8.0.2.0.0',
    'category': 'Customer Relationship Management',
    'website': 'https://odoo-community.org/',
    'author': 'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': ['mail'],
    'data': [
        'views/res_letter_view.xml',
        'views/letter_category_view.xml',
        'views/letter_type_view.xml',
        'views/letter_channel_view.xml',
        'views/letter_folder_view.xml',
        'views/letter_reassignment_view.xml',
        'data/letter_sequence.xml',
        'security/ir.model.access.csv',
        'security/lettermgmt_security.xml',
    ],
    'demo': ['data/letter_demo.xml'],
}
