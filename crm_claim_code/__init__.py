# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from . import models
from openerp.api import Environment
from openerp import SUPERUSER_ID


def create_code_equal_to_id(cr):
    cr.execute("SELECT column_name FROM information_schema.columns "
               "WHERE table_name = 'crm_claim' AND column_name = 'code'")
    if not cr.fetchone():
        cr.execute('ALTER TABLE crm_claim '
                   'ADD COLUMN code character varying;')
        cr.execute('UPDATE crm_claim '
                   'SET code = id;')


def assign_old_sequences(cr, registry):
    with Environment.manage():
        env = Environment(cr, SUPERUSER_ID, {})

        sequence_model = env['ir.sequence']

        claims = env['crm.claim'].search([], order="id")
        for claim in claims:
            claim.code = sequence_model.next_by_code('crm.claim')
