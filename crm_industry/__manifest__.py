# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Industry",
    "summary": "Link leads/opportunities to industries",
    "version": "13.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["crm", "partner_industry_secondary"],
    "data": ["views/crm_lead_view.xml"],
}
