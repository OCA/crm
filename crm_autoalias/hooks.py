# -*- coding: utf-8 -*-
# © 2016 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from uuid import uuid4
from openerp import SUPERUSER_ID


def assign_alias_to_crm(cr, registry):
    lead_registry = registry['crm.lead']
    mail_alias_registry = registry['mail.alias']
    ir_model_registry = registry['ir.model']
    lead_model_ids = ir_model_registry.search(cr, SUPERUSER_ID, [
        ('model', '=', 'crm.lead')
    ])
    lead_ids = lead_registry.search(cr, SUPERUSER_ID, [
        ('email_alias', '=', False)
    ])
    for lead_id in lead_ids:
        while True:
            alias_name = "{0}-crm".format(uuid4().hex)
            mail_alias_ids = mail_alias_registry.search(cr, SUPERUSER_ID, [
                ('alias_name', '=', alias_name)
            ])
            if not mail_alias_ids:
                break
        alias_id = mail_alias_registry.create(cr, SUPERUSER_ID, {
            'alias_name': alias_name,
            'alias_model_id': lead_model_ids[0]
        })
        lead_registry.write(cr, SUPERUSER_ID, [lead_id], {
            'email_alias': alias_id
        })
