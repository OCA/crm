# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from . import models
from openerp import SUPERUSER_ID


def create_code_equal_to_id(cr):
    cr.execute('ALTER TABLE crm_lead '
               'ADD COLUMN code character varying;')
    cr.execute('UPDATE crm_lead '
               'SET code = id;')


def assign_old_sequences(cr, registry):
    lead_obj = registry['crm.lead']
    sequence_obj = registry['ir.sequence']
    lead_ids = lead_obj.search(cr, SUPERUSER_ID, [], order="id")
    for lead_id in lead_ids:
        cr.execute('UPDATE crm_lead '
                   'SET code = \'%s\' '
                   'WHERE id = %d;' %
                   (sequence_obj.get(cr, SUPERUSER_ID, 'crm.lead'), lead_id))
