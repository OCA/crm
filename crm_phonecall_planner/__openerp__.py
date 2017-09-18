# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Phonecall planner",
    "summary": "Schedule phone calls according to some criteria",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm_phonecall",
    ],
    "data": [
        "wizards/crm_phonecall_planner_view.xml",
    ],
}
