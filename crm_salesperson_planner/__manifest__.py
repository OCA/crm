# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Crm Salesperson Planner",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Customer Relationship Management",
    "author": "Sygel Technology," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm", "calendar"],
    "data": [
        "data/crm_salesperson_planner_sequence.xml",
        "wizards/crm_salesperson_planner_visit_close_wiz_view.xml",
        "wizards/crm_salesperson_planner_visit_template_create.xml",
        "views/crm_salesperson_planner_visit_views.xml",
        "views/crm_salesperson_planner_visit_close_reason_views.xml",
        "views/crm_salesperson_planner_visit_template_views.xml",
        "views/crm_salesperson_planner_menu.xml",
        "views/res_partner.xml",
        "views/crm_lead.xml",
        "data/ir_cron_data.xml",
        "security/crm_salesperson_planner_security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
