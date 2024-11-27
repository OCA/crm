# Copyright 2019 Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CRM Lead Currency",
    "summary": """
        On leads/opportunities, add the amount in the customer's currency.""",
    "maintainers": [
        "luisg123v",
    ],
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp SA,Odoo Community Association (OCA),Vauxoo",
    "website": "https://github.com/OCA/crm",
    "depends": [
        "crm",
    ],
    "data": [
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
