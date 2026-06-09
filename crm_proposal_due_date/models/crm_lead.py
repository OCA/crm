# Copyright 2026 Ctrl-a
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models

_ACTIVITY_XMLID = "crm_proposal_due_date.mail_activity_type_proposal"


class CrmLead(models.Model):
    _inherit = "crm.lead"

    proposal_due_date = fields.Date(
        string="Expected Proposal Submission Date",
        tracking=True,
        index=True,
    )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.proposal_due_date:
                record._sync_proposal_activity()
        return records

    def write(self, vals):
        if "proposal_due_date" not in vals:
            return super().write(vals)
        # Track which records already had a date before writing
        already_set_ids = set(self.filtered("proposal_due_date").ids)
        res = super().write(vals)
        for record in self:
            record._sync_proposal_activity(was_already_set=record.id in already_set_ids)
        return res

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _sync_proposal_activity(self, was_already_set=False):
        """Create or remove the 'Submit Proposal' activity.

        The activity deadline is managed independently by the user and is
        never overwritten when ``proposal_due_date`` changes.

        - First time ``proposal_due_date`` is set: schedule a new activity.
        - ``proposal_due_date`` changed (was already set): leave the existing
          activity untouched.
        - ``proposal_due_date`` cleared: remove any automated activity of this
          type.
        """
        self.ensure_one()
        activity_type = self.env.ref(_ACTIVITY_XMLID, raise_if_not_found=False)
        if not activity_type:
            return

        existing = self.activity_ids.filtered(
            lambda a: a.activity_type_id == activity_type and a.automated
        )

        if not self.proposal_due_date:
            existing.unlink()
            return

        if not existing and not was_already_set:
            # Only schedule when the date is set for the first time
            self.activity_schedule(
                act_type_xmlid=_ACTIVITY_XMLID,
                date_deadline=self.proposal_due_date,
                summary=_("Submit Proposal"),
            )
