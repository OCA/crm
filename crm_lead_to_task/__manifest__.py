# Copyright 2010-2020 Odoo S. A.
# Copyright 2021 Tecnativa - Pedro M. Baeza
# Copyright 2023-2024 Tecnativa - Carolina Fernandez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Lead to Task",
    "summary": "Create Tasks from Leads/Opportunities",
    "sequence": "19",
    "category": "Project",
    "complexity": "easy",
    "author": "Odoo S.A., Odoo Community Association (OCA), Tecnativa",
    "website": "https://github.com/OCA/crm",
    "depends": ["crm", "project"],
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/crm_lead_convert2task_views.xml",
        "views/crm_lead_views.xml",
    ],
}
