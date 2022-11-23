# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Klaviyo API",
    "summary": "Manage Klaviyo API keys",
    "version": "12.0.1.0.0",
    "development_status": "Alpha",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            # this is for compatibility with py3.6
            'dataclasses',
            'klaviyo_api',
        ],
    },
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/klaviyo_account.xml",
    ],
}
