# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "CRM stage probability",
    "summary": "Define fixed probability on the stages",
    "version": "13.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Camptocamp, Odoo Community Association (OCA), Odoo SA",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "views/crm_lead.xml",
        "views/crm_stage.xml",
        "wizard/crm_lead_stage_probability_update.xml",
        "data/crm_stage.xml",
    ],
}
