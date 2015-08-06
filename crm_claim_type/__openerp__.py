# -*- coding: utf-8 -*-
{
    'name': 'CRM Claim Types',
    'category': 'Customer Relationship Management',
    'summary': 'Claim types for CRM',
    'author': 'Vauxoo',
    'website': 'www.vauxoo.com',
    'description': """
    Allows to set and maintain claim types for CRM Claims
    """,
    'depends': [
        'base',
        'crm_claim',
    ],
    'security': [
        'security/ir.model.access.csv',
    ],
    'data': [
        'views/crm_claim_type_view.xml',
        'data/crm_claim_type_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
