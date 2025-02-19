# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "SRM",
    "summary": "Use CRM model for suppliers",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account",
        "crm",
        "sale_crm",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/srm_menu.xml",
        "views/srm_lead.xml",
        "views/crm_lead.xml",
        "views/purchase_order.xml",
        "wizard/srm_opportunity_to_rfq.xml",
    ],
    "installable": True,
}
