# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2017 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Tracking Fields in Partners",
    "summary": "Copy tracking fields from leads to partners",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://www.github.com/oca/crm",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
    "images": [
        "images/.png",
    ],
}
