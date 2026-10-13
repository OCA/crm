# Copyright 2026  Akretion (https://www.akretion.com).
# @author Sébastien Alix <sebastien.alix@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    "name": "Sales Team Readonly",
    "summary": "Read-only group shared by the Sales applications",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/OCA/crm",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": [
        "sales_team",
    ],
    "data": [
        "security/res_groups.xml",
    ],
    "installable": True,
}
