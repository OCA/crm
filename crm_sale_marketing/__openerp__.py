# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales Marketing",
    "summary": "Marketing Details of Sales",
    "version": "8.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "https://odoo-community.org/",
    "category": "Hidden",
    'data': [
        'security/ir.model.access.csv',
    ],
    "depends": ["sale_crm", "marketing"],
    "license": "AGPL-3",
    'installable': True,
}
