##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from . import models
from odoo import api, SUPERUSER_ID


def create_code_equal_to_id(env):
    env.cr.execute("ALTER TABLE crm_lead ADD COLUMN code character varying;")
    env.cr.execute("UPDATE crm_lead SET code = id;")


def assign_old_sequences(env):
    lead_obj = env["crm.lead"]
    sequence_obj = env["ir.sequence"]
    leads = lead_obj.search([], order="id")
    for lead_id in leads.ids:
        env.cr.execute(
            "UPDATE crm_lead SET code = %s WHERE id = %s;",
            (
                sequence_obj.next_by_code("crm.lead"),
                lead_id,
            ),
        )
