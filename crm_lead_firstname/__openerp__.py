# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Firstname and Lastname in Leads",
    "summary": "Specify split names for contacts in leads",
    "version": "8.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "partner_firstname",
    ],
    "data": [
        "views/crm_lead_view.xml",
    ],
}
