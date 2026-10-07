# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "CRM Project Create From Template",
    "summary": "Create projects from CRM using a project template",
    "version": "18.0.1.0.0",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm_project_create", "project_template"],
    "data": ["wizards/crm_create_project.xml"],
    "maintainers": ["edescalona"],
}
