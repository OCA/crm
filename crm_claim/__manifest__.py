# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Claims Management",
    "version": "13.0.1.0.1",
    "category": "Customer Relationship Management",
    "author": "Odoo S.A., " "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "summary": "Track your customers/vendors claims and grievances.",
    "depends": ["crm", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/crm_claim_security.xml",
        "data/crm_claim_data.xml",
        "views/crm_claim_views.xml",
        "views/crm_claim_category_views.xml",
        "views/crm_claim_stage_views.xml",
        "views/res_partner_views.xml",
        "views/crm_claim_menu.xml",
        "report/crm_claim_report_view.xml",
    ],
    "demo": ["demo/crm_claim_demo.xml"],
    "installable": True,
}
