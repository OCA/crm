# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    def _reset_lead_followup(self):
        """Restart the escalation clock of the leads of these activities."""
        activities = self.filtered(lambda activity: activity.res_model == "crm.lead")
        if activities:
            leads = self.env["crm.lead"].browse(activities.mapped("res_id"))
            leads.exists()._reset_followup()

    @api.model_create_multi
    def create(self, vals_list):
        activities = super().create(vals_list)
        # A salesperson planning a call or a meeting on a lead is working on
        # it, so the lead must not be escalated as stalled. Automated
        # activities are planned by modules on their own: they would keep the
        # escalation clock reset forever.
        activities.filtered(
            lambda activity: not activity.automated
        )._reset_lead_followup()
        return activities

    def _action_done(self, feedback=False, attachment_ids=None):
        # Completing an activity, even an automated one such as the escalation
        # itself, is always somebody working on the lead.
        self._reset_lead_followup()
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)
