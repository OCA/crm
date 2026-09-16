# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, fields, models

FOLLOWUP_RESET_FIELDS = {"stage_id", "user_id"}


class CrmLead(models.Model):
    _inherit = "crm.lead"

    last_followup_date = fields.Datetime(
        string="Last Follow-up",
        default=lambda self: self.env.cr.now(),
        readonly=True,
        copy=False,
        index=True,
        help="Last time somebody worked on this lead: a message, a planned or "
        "completed activity, a stage change or a new salesperson.",
    )
    escalation_rule_ids = fields.Many2many(
        "crm.lead.escalation.rule",
        string="Applied Escalation Rules",
        readonly=True,
        copy=False,
    )

    def write(self, vals):
        changed_fields = FOLLOWUP_RESET_FIELDS & vals.keys()
        # Rewriting a field with the value it already holds is not a follow-up.
        to_reset = self.filtered(
            lambda lead: any(
                lead[name].id != (vals[name] or False) for name in changed_fields
            )
        )
        res = super().write(vals)
        if to_reset:
            to_reset._reset_followup()
        return res

    def message_post(self, **kwargs):
        message = super().message_post(**kwargs)
        if kwargs.get("message_type", "notification") in ("comment", "email"):
            self._reset_followup()
        return message

    def _reset_followup(self):
        """Restart the escalation clock and allow the rules to fire again."""
        if self.env.context.get("crm_lead_escalation"):
            return
        leads = self.filtered(lambda lead: lead.won_status == "pending")
        if not leads:
            return
        # Technical fields: whoever may post on the lead may reset its clock,
        # even without write access on the lead itself.
        leads.sudo().write(
            {
                "last_followup_date": self.env.cr.now(),
                "escalation_rule_ids": [Command.clear()],
            }
        )
