# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Email Template Configurator',
    'description': """
        Simplifies use of placeholders in email templates""",
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/crm',
    'depends': [
        'email_template',
    ],
    'data': [
        'security/email_template_placeholder.xml',
        'views/email_template_placeholder.xml',
        'views/email_template.xml',
    ],
}
