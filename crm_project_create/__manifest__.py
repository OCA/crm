# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "CRM Project Create",
    "summary": "Allow create projects from lead/opportunity",
    "version": "18.0.1.0.1",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["EmilioPascual", "rafaelbn"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm", "sale_project", "mail_message_destiny_link_template"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/crm_create_project.xml",
        "views/crm_lead.xml",
    ],
}
