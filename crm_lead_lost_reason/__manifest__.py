# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM - Lost Reason",
    "summary": "Always add lost reasons to leads/opportunities",
    "version": "15.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "data/ir_actions_server.xml",
        "views/crm_lead.xml",
    ],
}
