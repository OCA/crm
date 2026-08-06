# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM - Fix lead currency",
    "summary": "Fixes usage of leads' currencies",
    "version": "19.0.1.0.0",
    "category": "Sales/CRM",
    "website": "https://github.com/OCA/crm",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": [
        # Odoo
        "crm",
    ],
    # Make sure this module is installed as soon as possible
    # after ``crm`` is installed: this way, the override of
    # ``crm.lead._field_to_sql()`` will work correctly
    "sequence": 0,
}
