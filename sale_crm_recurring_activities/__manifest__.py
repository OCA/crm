{
    "name": "Sale CRM recurring activities",
    "summary": """
        Add recurring activities to opportunity after quotation has been confirmed
    """,
    "author": "PyTech SRL, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/crm",
    "category": "Hidden",
    "version": "16.0.1.0.0",
    "depends": [
        "html_text",
        "sale_crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rules.xml",
        "views/crm_recurring_activity_views.xml",
    ],
    "installable": True,
}
