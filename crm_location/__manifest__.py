# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria - Endika Iglesias <endikaig@antiun.com>
# Copyright 2017 Tecnativa - Luis Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'CRM location',
    'category': 'Customer Relationship Management',
    'version': '10.0.1.0.0',
    'depends': [
        'crm',
        'base_location',
    ],
    'data': ['views/crm_lead_view.xml'],
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://www.tecnativa.com',
    'license': 'AGPL-3',
    'installable': True,
}
