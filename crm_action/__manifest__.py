# -*- coding: utf-8 -*-
# Copyright Savoir-faire Linux, Equitania Software GmbH, Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CRM Action',
    'version': '10.0.1.2.0',
    'author': 'Savoir-faire Linux, Equitania Software GmbH, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Others',    'license': 'AGPL-3',
    'depends': ['base_setup', 'crm', 'sales_team'],
    'category': 'Others',
    'summary': 'CRM Action',

    'data': [
        'security/res_groups_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        'views/crm_action_type_view.xml',
        'views/crm_action_view.xml',
        'views/crm_lead_view.xml',
        'views/crm_opportunity_view.xml',
    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
