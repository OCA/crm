# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "CRM won reason",
    "version": "15.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/crm_lead_won.xml",
        "views/crm_views.xml",
    ],
    "installable": True,
    "maintainers": ["ajaniszewska-dev"],
}
