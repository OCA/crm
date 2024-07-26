# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "CRM Referred",
    "summary": "Categorise lead/oppportunity according to referred by",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["EmilioPascual", "rafaelbn"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_referred.xml",
        "views/crm_lead.xml",
        "views/res_partner.xml",
    ],
}
