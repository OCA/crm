# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "CRM Lead Project",
    "summary": "Create a project when converting lead into opportunity",
    "version": "10.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/OCA/crm",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "project",
    ],
    "data": [
        "wizard/crm_opportunity_create_project.xml",
        "views/crm_lead.xml",
        "views/crm_project.xml",
        "views/project.xml",
        "wizard/crm_lead_to_opportunity.xml",
    ],
}
