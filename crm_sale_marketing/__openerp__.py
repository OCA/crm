# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales Marketing",
    "summary": "Marketing Details of Sales",
    'description': """
This module copies the marketing details while converting opportunity to
quotation. This will help to know that how many Sales are generated from
the any particular campaign.
    """,
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Hidden",
    "depends": ["sale_crm"],
    "data": ['views/crm_sale_marketing.xml'],
    "license": "AGPL-3",
    'installable': True,
}
