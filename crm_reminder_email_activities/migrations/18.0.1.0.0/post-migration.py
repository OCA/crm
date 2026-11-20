from dateutil.relativedelta import relativedelta
from openupgradelib import openupgrade

from odoo import fields

# ruff: noqa: E501
new_body_en = """
    <div>
        <span style="font-size: 0.75rem;">Reminder CRM planned activities
        </span>
        <br />
        <span style="font-size: 1.3rem; font-weight: bold;margin-top: 14px;">
        <t t-out="object.name or ''">User</t>
        </span>
        <div style="font-size: 0.9rem">
            <p>
                Dear  <t t-out="object.name or ''">User</t>,                <br />
                Below are your active CRM app tasks due in the next 7 days:<br />
                <ul>
                    <t t-set="activities" t-value="ctx.get('activities', '')" />
                    <t t-foreach="activities" t-as="activity">
                        <li>
                            <t
                                t-set="activity_obj"
                                t-value="object.env[activity.res_model].browse(activity.res_id)"
                            />
                            <p style="margin-bottom:0 !important;">Deadline:
                                <span
                                t-field="activity.date_deadline"
                                t-options="{'widget': 'date'}"
                            />
                            </p>
                            <p style="margin:0 !important;">
                                <span t-out="activity_obj.display_name" />
                                        -
                                <span
                                t-out="activity.summary or activity_obj.activity_type_id.display_name"
                            />
                            </p>
                        </li>
                    </t>
                </ul>
            </p>
        </div>
    </div>
"""


def _update_crm_mail_template(env):
    mail_template = env.ref(
        "crm_reminder_email_activities.email_template_crm_reminder_activities"
    )
    mail_template_en = mail_template.with_context(lang="en_US")
    mail_template_en.write(
        {
            "body_html": new_body_en,
            "lang": "{{ object.partner_id.lang }}",
        }
    )


def _update_crm_cron_job(env):
    crm_cron_job = env.ref(
        "crm_reminder_email_activities.crm_email_reminder_activities_cron"
    )
    ir_model_item = env["ir.model"]._get("crm.lead")
    crm_cron_job.write(
        {
            "model_id": ir_model_item.id,
            "code": "model.cron_send_activities_reminder()",
            "nextcall": fields.Datetime.now() + relativedelta(weekday=6),
        }
    )


@openupgrade.migrate()
def migrate(env, version):
    _update_crm_cron_job(env)
    _update_crm_mail_template(env)
