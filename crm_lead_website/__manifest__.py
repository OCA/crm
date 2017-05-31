# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website in leads",
    "summary": "Add Website field to leads",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://www.tecnativa.com",
    "author": "Antiun Ingeniería S.L., "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "views/crm_lead.xml",
    ],
}
