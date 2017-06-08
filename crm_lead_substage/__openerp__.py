# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Substages in leads/opportunities",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "Antiun Ingeniería S.L., "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "website": "https://www.antiun.com",
    "category": "Customer Relationship Management",
    "depends": [
        'crm',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/crm_substage_view.xml',
        'report/crm_lead_report_view.xml',
        'report/crm_opportunity_report_view.xml',
    ],
    "installable": True,
}
