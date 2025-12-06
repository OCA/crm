# Copyright 2025 Teacnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "CRM stage multiple teams ",
    "summary": "Allows multiple teams in crm stage",
    "version": "18.0.1.0.1",
    "development_status": "Alpha",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, Odoo Community Association (OCA), Odoo SA",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "views/crm_stage_views.xml",
        "views/crm_lead_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
