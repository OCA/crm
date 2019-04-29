# Copyright 2019 Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CRM Opportunity Currency',
    'summary': """
        On opportunities add the amount in the company currency.""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp SA,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/crm',
    'depends': [
        'crm',
    ],
    'data': [
        'views/crm_lead_opportunity_currency_views.xml',
    ],
    'installable': True,
}
