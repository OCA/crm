# @@ -1,11 +1,10 @@
# Copyright 2017 Tecnativa - Vicent Cubells

{
    "name": "CRM Phone Calls",
    "version": "17.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Odoo S.A., Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm", "calendar"],
    "data": [
        "security/crm_security.xml",
        "security/ir.model.access.csv",
        "wizard/crm_phonecall_to_phonecall_view.xml",
        "views/crm_phonecall_view.xml",
        "views/res_partner_view.xml",
        "views/crm_lead_view.xml",
        "views/res_config_settings_views.xml",
        "report/crm_phonecall_report_view.xml",
    ],
    "installable": True,
}
