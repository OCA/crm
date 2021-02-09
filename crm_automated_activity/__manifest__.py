# Copyright 2021 Eder Brito
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CRM Automated Activity',
    'summary': """
        Automated Activities for CRM Stages""",
    'version': '13.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Eder Brito,Odoo Community Association (OCA)',
    'website': 'pingotecnologia.com.br',
    'depends': [
        'crm',
    ],
    'data': [
        'security/automated_activity.xml',
        'views/crm_stage.xml',
        'views/automated_activity.xml',
    ],
    'demo': [
    ],
}
