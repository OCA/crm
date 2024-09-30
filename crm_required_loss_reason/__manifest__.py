# Copyright 2024 Jarsa - Alan Ramos
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "CRM Required Loss Reason",
    "summary": "Make loss reason required in wizard",
    "version": "16.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm"],
    "maintainers": ["alan196"],
    "data": [
        "wizards/crm_lead_lost_views.xml",
    ],
}
