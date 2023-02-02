# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM Multicompany Reporting Currency",
    "summary": "Adds Amount in multicompany reporting currency to CRM Lead",
    "version": "15.0.1.0.3",
    "category": "Sales",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["crm", "base_multicompany_reporting_currency"],
    "website": "https://github.com/OCA/crm",
    "data": ["views/crm_lead_views.xml"],
    "installable": True,
    "maintainers": ["yankinmax"],
}
