{
    "name": "CRM Stage Project Task",
    "version": "17.0.1.0.0",
    "category": "Sales/CRM",
    "summary": """
    Automatically assigns pre-defined task templates when
    moving CRM leads/opportunities through pipeline stages.
    """,
    "author": "XXP, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_views.xml",
        "views/crm_stage_views.xml",
        "views/project_task_views.xml",
        "views/crm_task_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
