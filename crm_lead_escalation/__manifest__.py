# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "CRM Lead Escalation",
    "summary": "Notify a manager when a lead is not followed up or not closed in time",
    "version": "19.0.1.0.0",
    "category": "Sales/CRM",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "security/ir.model.access.csv",
        "security/crm_lead_escalation_rule_rules.xml",
        "views/crm_lead_escalation_rule_views.xml",
        "views/crm_lead_views.xml",
        "views/res_config_settings_views.xml",
        "data/mail_template_data.xml",
        "data/ir_cron_data.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["JasminSForgeFlow"],
    "installable": True,
}
