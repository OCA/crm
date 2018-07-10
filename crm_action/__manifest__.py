# -*- coding: utf-8 -*-
# Copyright 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 RGB Consulting <http://odoo.rgbconsulting.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CRM Action',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux, '
              'Tecnativa, '
              'RGB Consulting, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'CRM',
    'summary': 'Adds action management in CRM',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        'views/crm_action_view.xml',
        'views/crm_action_type_view.xml',
        'views/crm_lead_view.xml',
        'data/email_reminder.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
