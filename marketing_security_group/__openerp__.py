# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Antonio Espinosa
# See README.rst file on addon root folder for more details

{
    'name': "Marketing security extra rules",
    'category': 'Marketing',
    'version': '8.0.1.0.0',
    'depends': [
        'marketing',
        'mass_mailing',
    ],
    'external_dependencies': {},
    'data': [
        'security/ir.model.access.csv',
        'security/mail_mass_mailing_security.xml',
    ],
    'author': 'Antiun Ingeniería S.L., '
              'Odoo Community Association (OCA)',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'demo': [],
    'test': [],
    'installable': True,
}
