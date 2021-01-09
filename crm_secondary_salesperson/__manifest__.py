# Copyright 2020 - TODAY, Escodoo - https://www.escodoo.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Crm Secondary Salesperson',
    'category': 'Customer Relationship Management',
    'summary': """
        CRM Secondary Salesperson""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo, Odoo Community Association (OCA)',
    'maintainers': ['marcelsavegnago'],
    'website': 'https://github.com/OCA/crm',
    'images': ['static/description/banner.png'],
    'depends': [
        'crm',
    ],
    'data': [
        'views/crm_lead.xml',
    ],
}
