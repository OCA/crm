# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Crm Lead Sequence',
    'summary': """
        This addon add a sequence to crm leads""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/crm',
    'depends': ["crm"],
    'data': [
        'data/crm_lead_sequence.xml',
        'views/crm_lead.xml'
    ],
    'demo': [],
    "post_init_hook": "init_lead_ref",

}
