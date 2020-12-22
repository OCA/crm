# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CRM Lead Type",
    "version": "14.0.1.0.0",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "summary": "CRM Lead Type",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm", "sales_team"],
    "category": "Sales/CRM",
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_type_views.xml",
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
