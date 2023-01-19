# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CRM Lead to opportunity - Contact",
    "version": "14.0.1.0.0",
    "category": "CRM",
    "license": "AGPL-3",
    "summary": "Lead to opportunity: option to create a contact on an existing "
    "customer",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/crm",
    "depends": ["crm"],
    "data": [
        "wizards/crm_lead_to_opportunity_view.xml",
    ],
    "installable": True,
}
