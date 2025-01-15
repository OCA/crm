# Copyright 2024 INVITU SARL
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM Lead Approval",
    "summary": "This module allows to approve or not a lead.",
    "version": "17.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "INVITU SARL, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/crm",
    "depends": [
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "wizard/approval_wizard_views.xml",
        "views/crm_lead_views.xml",
    ],
}
