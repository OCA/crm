# Copyright 2026 Ctrl-a
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "CRM Proposal Due Date",
    "summary": "Track proposal submission date and auto-schedule a dedicated activity",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Ctrl-a, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "data/mail_activity_type.xml",
        "views/crm_lead_view.xml",
    ],
}
