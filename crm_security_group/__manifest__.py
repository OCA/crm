# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "CRM Only Security Groups",
    "summary": "Add new group in Sales to show only CRM",
    "version": "14.0.1.1.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm", "sale_crm"],
    # sale_crm dependency is necessary to add groups in some view
    "maintainers": ["victoralmau"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu_items.xml",
    ],
}
