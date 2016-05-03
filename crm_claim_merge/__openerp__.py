# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    'name': 'Claims Merge',
    'version': '9.0.1.0.0',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'maintainer': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Customer Relationship Management',
    'depends': [
        'crm_claim'
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        'wizard/crm_claim_merge_view.xml',
    ],
    'test': [
        'test/crm_claim_merge.yml',
    ],
    'installable': True,
    'auto_install': False,
}
