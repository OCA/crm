# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    if not version:
        return

    cr.execute(
        'ALTER TABLE "crm_action_type" RENAME "is_active" TO "active"')

    cr.execute(
        'ALTER TABLE "crm_action" RENAME "action_type" TO "action_type_id"')
