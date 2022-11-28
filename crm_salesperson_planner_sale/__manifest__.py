# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Crm Salesperson Planner Sale",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Customer Relationship Management",
    "author": "Sygel Technology, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm_salesperson_planner", "sale"],
    "data": [
        "views/sale_order_views.xml",
        "views/crm_salesperson_planner_visit_views.xml",
    ],
    "installable": True,
}
