# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


XMLID_RENAMES = [
    ('crm.group_scheduled_calls', 'crm_phonecall.group_scheduled_calls'),
    ('crm.filter_crm_phonecall_sales_team',
     'crm_phonecall.filter_crm_phonecall_sales_team'),
    ('crm.filter_crm_phonecall_delay_to_close',
     'crm_phonecall.filter_crm_phonecall_delay_to_close'),
    ('crm.filter_crm_phonecall_phone_call_to_do',
     'crm_phonecall.filter_crm_phonecall_phone_call_to_do'),
]


def migrate(cr, version):
    # This is not decorated with @openupgrade.migrate as the module is being
    # installed and thus, the migration script should be run unconditionally
    openupgrade.rename_xmlids(cr, XMLID_RENAMES)
