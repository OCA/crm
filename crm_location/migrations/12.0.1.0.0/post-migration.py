# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2 import sql
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Link crm.lead with corresponding new entries
    openupgrade.logged_query(env.cr, sql.SQL(
        """UPDATE crm_lead cl
        SET location_id = rcz.id
        FROM res_city_zip rcz
        WHERE rcz.{} = cl.{}"""
    ).format(
        sql.Identifier(openupgrade.get_legacy_name('better_zip_id')),
        sql.Identifier(openupgrade.get_legacy_name('location_id')),
    ))
