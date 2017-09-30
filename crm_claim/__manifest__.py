# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "Claims Management",
    "version": "10.0.1.0.0",
    "category": "Sales",
    "depends": ["crm", "sales_team"],
    "data": [
        "views/crm_claim_view.xml",
        "views/crm_claim_menu.xml",
        "security/ir.model.access.csv",
        "report/crm_claim_report_view.xml",
        "data/crm_claim_data.xml",
        "views/res_partner_view.xml",
    ],
    "demo": [
        "demo/crm_claim_demo.xml"
    ],
    "test": [
#        "test/process/claim.yml",
#        "test/ui/claim_demo.yml",
    ],
    "installable": True,
    "auto_install": False,
}
