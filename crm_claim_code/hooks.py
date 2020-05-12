# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.api import Environment
from odoo import SUPERUSER_ID


new_field_code_added = False


def create_code_equal_to_id(cr):
    cr.execute("SELECT column_name FROM information_schema.columns "
               "WHERE table_name = 'crm_claim' AND column_name = 'code'")
    if not cr.fetchone():
        cr.execute('ALTER TABLE crm_claim '
                   'ADD COLUMN code character varying;')
        cr.execute('UPDATE crm_claim '
                   'SET code = id;')
        global new_field_code_added
        new_field_code_added = True


def assign_old_sequences(cr, registry):
    if not new_field_code_added:
        # the field was already existing before the installation of the addon
        return
    with Environment.manage():
        env = Environment(cr, SUPERUSER_ID, {})

        sequence_model = env['ir.sequence']

        claims = env['crm.claim'].search([], order="id")
        for claim in claims:
            claim.code = sequence_model.next_by_code('crm.claim')
