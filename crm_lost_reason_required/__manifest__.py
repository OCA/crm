# Copyright 2025 Hector del Reguero
# Copyright 2026 Gray Matter Logic
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "CRM Lost Reason Required",
    "version": "19.0.1.0.0",
    "category": "Customer Relationship Management",
    "summary": "Make the lost reason mandatory when marking a lead/opportunity as lost",
    "author": "Hector del Reguero, Gray Matter Logic, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "LGPL-3",
    "depends": ["crm"],
    "data": [
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
