# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from . import models
from openerp import SUPERUSER_ID


def assign_old_sequences(cr, registry):
    cr.execute("""
        SELECT True
        FROM information_schema.columns
        WHERE table_name='crm_claim' AND column_name='sequence'
    """)
    found = cr.fetchall()
    if found and found[0]:
        cr.execute("""
            UPDATE crm_claim
            SET code = sequence
            WHERE code IS NULL OR code = '/'
        """)
