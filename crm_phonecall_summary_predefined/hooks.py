# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError


def convert_names_to_many2one(env):  # pragma: no cover
    """Convert old string names to new Many2one"""
    summary = env["crm.phonecall.summary"]
    phone_call = env["crm.phonecall"]
    for s in phone_call.search([("summary_id", "=", False)]):
        try:
            with env.cr.savepoint():
                s.summary_id = summary.create({"name": s.name})
        except IntegrityError:
            s.summary_id = summary.search([("name", "=", s.name)])
