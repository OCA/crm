# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Phone Calls",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Odoo S.A., "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "http://www.tecnativa.com",
    "license": "AGPL-3",
    "depends": [
        'crm',
        'calendar',
    ],
    "data": [
        'security/crm_security.xml',
        'security/ir.model.access.csv',
        'wizard/crm_phonecall_to_phonecall_view.xml',
        'views/crm_phonecall_view.xml',
        'views/res_partner_view.xml',
        'views/crm_lead_view.xml',
        'report/crm_phonecall_report_view.xml',
    ],
    'installable': True,
}
