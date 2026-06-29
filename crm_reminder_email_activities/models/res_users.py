from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def cron_send_crm_reminder_activities(self):
        users = self._get_crm_activities().mapped("user_id")
        mail_template = self.env.ref(
            "crm_reminder_email_activities.email_template_crm_reminder_activities"
        )
        for user in users:
            mail_template.send_mail(user.id)

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
