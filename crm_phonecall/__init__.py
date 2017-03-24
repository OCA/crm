# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import models
from . import wizard
from . import report


xmlid_renames = [
    ('crm.group_scheduled_calls', 'crm_phonecall.group_scheduled_calls'),
    ('crm.filter_crm_phonecall_phone_call_to_do',
        'crm_phonecall.filter_crm_phonecall_phone_call_to_do'),
    ('crm.filter_crm_phonecall_delay_to_close',
        'crm_phonecall.filter_crm_phonecall_delay_to_close'),
    ('crm.filter_crm_phonecall_sales_team',
        'crm_phonecall.filter_crm_phonecall_sales_team'),
]


def column_exists(cr, table, column):
    cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s""", (table, column))
    return bool(cr.fetchall())


def rename_xmlids_hook(cr):
    # Retrieve column phone_id saved on crm migration
    if column_exists(cr, 'calendar_event', 'phone_id'):
        cr.execute("""
          ALTER TABLE calendar_event
              RENAME COLUMN openupgrade_legacy_90_phone_id TO phone_id""")
        from openupgradelib import openupgrade
        openupgrade.rename_xmlids(cr, xmlid_renames)
