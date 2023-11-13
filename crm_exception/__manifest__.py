# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "CRM Exception",
    "version": "16.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Quartile Limited, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "depends": ["crm", "base_exception"],
    "license": "AGPL-3",
    "data": [
        "views/crm_lead_views.xml",
        "views/base_exception_views.xml",
    ],
    "demo": [
        "demo/crm_exception_demo.xml",
    ],
    "installable": True,
}
