# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Claim Analytic",
    "version": "16.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "AvanzOSC, Trey, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "depends": [
        "analytic",
        "crm_claim",
    ],
    "data": [
        "views/account_analytic_account_view.xml",
        "views/account_analytic_line_view.xml",
        "views/crm_claim_view.xml",
    ],
}
