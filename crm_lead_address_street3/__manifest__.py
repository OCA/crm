# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Street3 in lead addresses',
    'version': '10.0.1.0.0',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'maintainer': 'Camptocamp',
    'category': 'Customer Relationship Management',
    'complexity': 'easy',
    'depends': ['partner_address_street3', 'crm'],
    'website': 'https://github.com/OCA/crm',
    'data': ['view/crm_lead_view.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
