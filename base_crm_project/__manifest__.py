# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Base CRM Project",
    "summary": "Link between Crm and Task",
    "version": "15.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["EmilioPascual"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "project",
    ],
    "data": [
        "views/crm_lead.xml",
        "views/project_task.xml",
    ],
}
