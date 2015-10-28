# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from . import models
from openerp import SUPERUSER_ID


def create_code_equal_to_id(cr):
    cr.execute('ALTER TABLE crm_claim '
               'ADD COLUMN code character varying;')
    cr.execute('UPDATE crm_claim '
               'SET code = id;')


def assign_old_sequences(cr, registry):
    claim_obj = registry['crm.claim']
    sequence_obj = registry['ir.sequence']
    claim_ids = claim_obj.search(cr, SUPERUSER_ID, [], order="id")
    for claim_id in claim_ids:
        cr.execute('UPDATE crm_claim '
                   'SET code = \'%s\' '
                   'WHERE id = %d;' %
                   (sequence_obj.get(cr, SUPERUSER_ID, 'crm.claim'), claim_id))
