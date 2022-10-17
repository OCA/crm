# Copyright 2022 Telmo Santos <telmo.santos@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "SRM",
    "version": "14.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "summary": "Use CRM model for suppliers",
    "license": "AGPL-3",
    "category": "CRM",
    "depends": [
        "account",
        "crm",
        "sale_crm",
        "purchase",
        "crm_enterprise",
    ],
    "website": "https://github.com/OCA/crm",
    "data": [
        "security/ir.model.access.csv",
        "views/srm_menu_views.xml",
        "views/srm_lead_views.xml",
        "views/crm_lead_views.xml",
        "views/purchase_views.xml",
        "wizard/srm_opportunity_to_rfq_views.xml",
    ],
    "installable": True,
}
