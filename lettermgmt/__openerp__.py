# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# © 2015 Holger Brunn <hbrunn@therp.nl>
# © 2009 Sandy Carter <sandy.carter@savoirfairelinux.com>
# © 2009 Parthiv Patel, Tech Receptives
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Letter Management',
    'version': '9.0.1.0.0',
    'author': "Odoo Community Association (OCA)",
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'category': 'Customer Relationship Management',
    'summary': 'Track letters, parcels, registered documents',
    'depends': ['mail'],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        "views/res_letter_view.xml",
        "views/letter_folder_view.xml",
        "views/letter_channel_view.xml",
        "views/letter_category_view.xml",
        "views/letter_reassignment_view.xml",
        "views/letter_type_view.xml",
        "data/letter_sequence.xml",
        'security/ir.model.access.csv',
    ],
    'demo': ["data/letter_demo.xml"],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
