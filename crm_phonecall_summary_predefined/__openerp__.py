# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Restricted Summary for Phone Calls",
    "summary": "Allows to choose from a defined summary list",
    "version": "8.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_phonecall_summary_view.xml",
        "views/crm_phonecall_view.xml",
    ],
    "images": [
        "images/summary_picker.png",
        "images/summary_editor.png",
    ],
}
