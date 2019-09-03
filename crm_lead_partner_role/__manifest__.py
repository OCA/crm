# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "CRM Lead Role",
    "summary": "Assign partner and roles to your leads",
    "version": "10.0.1.0.0",
    "category": "CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead.xml",
        "views/crm_role.xml",
    ],
}
