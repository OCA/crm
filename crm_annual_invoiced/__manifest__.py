# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Annual Invoiced Forecast",
    "summary": "Annual invoiced forecasts on sales widget",
    "version": "10.0.1.0.0",
    "category": "Sales",
    "website": "https://www.qubiq.es/",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "sale",
        "account",
    ],
    "data": [
        "views/crm_team_view.xml",
    ],
}
