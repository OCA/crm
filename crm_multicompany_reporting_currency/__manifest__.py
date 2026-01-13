# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM Multicompany Reporting Currency",
    "summary": "Adds Amount in multicompany reporting currency to CRM Lead",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        # OCA/crm
        "crm_lead_company_currency_fix",
        # OCA/sale-reporting
        "base_multicompany_reporting_currency",
    ],
    "website": "https://github.com/OCA/crm",
    "data": [
        # Views
        "views/crm_lead.xml"
    ],
    "installable": True,
    "maintainers": ["yankinmax"],
}
