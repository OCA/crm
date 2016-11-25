# -*- coding: utf-8 -*-
# © 2016 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Tracking Fields in Partners",
    "summary": "Copy tracking fields from leads to partners",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "marketing",
        "crm",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
    "images": [
        "images/.png",
    ],
}
