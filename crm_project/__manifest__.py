# Copyright 2010-2020 Odoo S. A.
# Copyright 2021 Tecnativa - Pedro M. Baeza
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Lead to Task",
    "summary": "Create Tasks from Leads/Opportunities",
    "sequence": "19",
    "category": "Project",
    "complexity": "easy",
    "data": ["wizard/crm_lead_convert2task_views.xml", "views/crm_lead_views.xml"],
    "author": "Odoo S.A., Odoo Community Association (OCA), Tecnativa",
    "depends": ["crm", "project"],
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "installable": True,
}
