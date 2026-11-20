from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def cron_send_activities_reminder(self):
        mail_template = self.env.ref(
            "crm_reminder_email_activities.email_template_crm_reminder_activities",
            raise_if_not_found=False,
        )
        if not mail_template:
            raise UserError(
                self.env._("CRM Reminder Activities Mail Template not found.")
            )

        activities = self._get_crm_activities()
        users = activities.mapped("user_id")
        for user in users:
            mail_template.with_context(activities=activities).send_mail(
                user.id,
                force_send=True,
                email_layout_xmlid="mail.mail_notification_light",
            )

    def _get_crm_activities(self, user=None):
        today = fields.Date.context_today(self)
        domain = [
            ("res_model", "=", "crm.lead"),
            ("date_deadline", ">=", today),
            ("date_deadline", "<=", today + relativedelta(days=+7)),
        ]
        if user:
            domain.append(("user_id", "=", user.id))
        return self.env["mail.activity"].search(domain, order="date_deadline asc")
