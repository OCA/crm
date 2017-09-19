# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


XMLID_RENAMES = [
    ('crm.group_scheduled_calls', 'crm_phonecall.group_scheduled_calls'),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, XMLID_RENAMES)
