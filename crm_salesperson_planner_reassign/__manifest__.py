# Copyright 2022 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Crm Salesperson Planner Reassign",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "category": "Customer Relationship Management",
    "author": "Sygel Technology," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm_salesperson_planner"],
    "data": [
        "security/ir.model.access.csv",
        "data/crm_salesperson_planner_reassign_sequence.xml",
        "views/crm_salesperson_planner_visit_reassign_views.xml",
        "views/crm_salesperson_planner_visit_template_views.xml",
        "views/crm_salesperson_planner_visit_views.xml",
    ],
    "installable": True,
}
