# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo import api, SUPERUSER_ID


def convert_names_to_many2one(cr, registry):  # pragma: no cover
    """Convert old string names to new Many2one"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        summary = env["crm.phonecall.summary"]
        phone_call = env["crm.phonecall"]
        for s in phone_call.search([("summary_id", "=", False)]):
            try:
                with env.cr.savepoint():
                    s.summary_id = summary.create({
                        "name": s.name,
                    })
            except IntegrityError:
                s.summary_id = summary.search([("name", "=", s.name)])
