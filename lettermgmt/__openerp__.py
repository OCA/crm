# -*- coding: utf-8 -*-
# copyright (C) 2013 Savoir-faire Linux <http://www.savoirfairelinux.com>
# Hardikgiri Goswami <hardikgiri.goswami@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Letter Management',
    'version': '9.0.1.0.0',
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'maintainer': 'Savoir-faire Linux, Hardikgiri Goswami',
    'website': 'http://www.savoirfairelinux.com',
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
    'test': [
        'test/res_letter.yml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
