# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "CRM Lead Partner Interest Group",
    "summary": "Manage interest groups on CRM leads and propagate them to the "
    "partner created from the lead.",
    "version": "19.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": [
        "crm",
        "partner_interest_group",
    ],
    "data": [
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
