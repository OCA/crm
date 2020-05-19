# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Stage Type",
    "summary": "Add type in the lead and opportunity stages",
    "version": "12.0.1.0.0",
    "category": "CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "views/crm_lead_views.xml",
        "views/crm_stage_views.xml",
    ],
}
