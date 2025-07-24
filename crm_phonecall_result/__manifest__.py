# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Crm Phonecall Result",
    "summary": "Adds phone call result tracking and reporting to CRM phonecalls",
    "version": "18.0.1.0.0",
    "category": "Partner Management",
    "website": "https://github.com/OCA/crm",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm_phonecall", "sales_team"],
    "data": [
        "security/ir.model.access.csv",
        "data/crm_phonecall_result_data.xml",
        "views/crm_phonecall_result_views.xml",
        "views/crm_phonecall_views.xml",
    ],
}
