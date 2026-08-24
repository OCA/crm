{
    "name": "CRM Reminder email activities",
    "summary": """
        This module periodically sends a reminder email for
        activities related to leads that expire within 7 days.
    """,
    "version": "18.0.1.0.0",
    "author": "PyTech SRL, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/crm",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "data/ir_cron.xml",
        "data/mail_template_reminder.xml",
    ],
}
