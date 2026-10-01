# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    def _get_escalation_leads(self):
        """Leads a person worked on through these activities.

        Automated activities are excluded: another module planning activities
        on its own would otherwise keep the escalation clock reset forever.
        """
        return self.env["crm.lead"].browse(
            [
                activity.res_id
                for activity in self
                if activity.res_model == "crm.lead" and not activity.automated
            ]
        )

    @api.model_create_multi
    def create(self, vals_list):
        activities = super().create(vals_list)
        # Planning a call or a meeting is working on the lead too.
        activities._get_escalation_leads().exists()._reset_followup()
        return activities

    def _action_done(self, feedback=False, attachment_ids=None):
        leads = self._get_escalation_leads()
        res = super()._action_done(feedback=feedback, attachment_ids=attachment_ids)
        leads.exists()._reset_followup()
        return res
