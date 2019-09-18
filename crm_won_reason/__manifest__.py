# Copyright 2019 RGB Consulting - Domantas Sidorenkovas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Crm Won Reason",
    'version': '12.0.1.0.0',
    'category': 'CRM',
    'depends': ['crm'],
    'author': "RGB Consulting,"
              "Odoo Community Association (OCA)",
    "maintainers": ["admin-rgbconsulting"],
    'license': 'AGPL-3',
    'website': "https://github.com/OCA/crm",
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_lead_won_view.xml',
        'views/crm_lead_view.xml',
        'views/crm_won_view.xml',
    ],
}
