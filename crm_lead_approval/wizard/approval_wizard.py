# Copyright 2024 INVITU SARL
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl.html).

from markupsafe import Markup

from odoo import fields, models
from odoo.tools.mail import is_html_empty


class CrmApprovalWizard(models.TransientModel):
    _name = "crm.approval.wizard"
    _description = "CRM Approval Wizard"

    lead_id = fields.Many2one("crm.lead", string="Opportunity", required=True)
    approval_comment = fields.Html(string="Observation", sanitize=True)

    def action_set_approve(self):
        self._update_lead_approval("done")

    def action_set_reserved(self):
        self._update_lead_approval("normal")

    def action_set_disapprove(self):
        self._update_lead_approval("blocked")

    def _update_lead_approval(self, status):
        self.ensure_one()
        self.lead_id.approval = status
        if not is_html_empty(self.approval_comment):
            self.lead_id._track_set_log_message(
                Markup('<div style="margin-bottom: 4px;"><p>%s:</p>%s<br /></div>')
                % ("Observation", self.approval_comment)
            )
        return {"type": "ir.actions.act_window_close"}
