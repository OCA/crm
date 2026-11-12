# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Crm Stage Analytic Account",
    "version": "18.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["crm", "analytic"],
    "data": [
        "data/ir_sequence_data.xml",
        "views/crm_stage_views.xml",
        "views/crm_lead_views.xml",
    ],
    "maintainers": ["CristianoMafraJunior"],
}
