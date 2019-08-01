# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    activity_type = env.ref('mail.mail_activity_data_todo')
    crm_claim_model = env.ref('crm_claim.model_crm_claim')
    cr.execute("""
        INSERT INTO
         mail_activity
           (res_model, res_model_id, res_id, res_name, user_id,
            date_deadline, summary, activity_type_id)
        SELECT
          %s,
          %s,
          id,
          name,
          COALESCE(user_id, create_uid),
          COALESCE(date_action_next, now()),
          action_next,
          %s
        FROM
          crm_claim
        WHERE
          date_action_next IS NOT Null
        OR
          action_next IS NOT Null;
    """, (crm_claim_model.model, crm_claim_model.id, activity_type.id))
