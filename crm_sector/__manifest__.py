# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Sector",
    "summary": "Link leads/opportunities to sectors",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "partner_sector",
    ],
    "data": [
        "views/crm_lead_view.xml",
    ]
}
