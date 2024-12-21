# Copyright 2024 Invitu SARL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM Tags Sales Team",
    "summary": "This module adds a filter by sales_team for crm_tags",
    "author": "INVITU, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "version": "17.0.1.0",
    "license": "AGPL-3",
    "category": "Customer Relationship Management",
    "depends": [
        "crm",
    ],
    "data": [
        "views/crm_tag_views.xml",
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
