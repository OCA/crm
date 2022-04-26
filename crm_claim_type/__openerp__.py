# -*- coding: utf-8 -*-
# © 2015 Vauxoo: Yanina Aular <yani@vauxoo.com>, Osval Reyes <osval@vauxoo.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CRM Claim Types',
    'category': 'Customer Relationship Management',
    'summary': 'Claim types for CRM',
    'author': 'Odoo Community Association (OCA),'
              'Vauxoo',
    'website': 'www.vauxoo.com',
    'license': 'AGPL-3',
    'version': '9.0.1.0.0',
    'depends': [
        'crm_claim',
    ],
    'data': [
        'data/crm_claim_type.xml',
        'data/crm_claim_stage.xml',
        'security/ir.model.access.csv',
        'views/crm_claim.xml',
        'views/crm_claim_stage.xml',
        'views/crm_claim_type.xml',
    ],
    'demo': [
        'demo/crm_claim.xml',
        'demo/crm_claim_stage.xml',
    ],
    'installable': True,
    'auto_install': False,
}
