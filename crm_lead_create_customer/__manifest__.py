# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "CRM Lead Create Customer",
    "summary": "Create the customer of an opportunity that was never a lead, "
    "reusing the standard conversion wizard.",
    "version": "19.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "LGPL-3",
    "depends": [
        "crm",
    ],
    "data": [
        "wizard/crm_lead2opportunity_partner_views.xml",
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
