# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

# Context flag set by crm.lead.action_create_customer, telling the wizard it
# was opened on a record that already is an opportunity.
CUSTOMER_ONLY_CONTEXT = "crm_lead_create_customer"


class CrmLead2opportunityPartner(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"

    has_duplicates = fields.Boolean(compute="_compute_has_duplicates")
    merge_duplicates = fields.Boolean(
        compute="_compute_merge_duplicates",
        store=True,
        readonly=False,
    )

    @api.depends("duplicated_lead_ids")
    def _compute_has_duplicates(self):
        for wizard in self:
            wizard.has_duplicates = len(wizard.duplicated_lead_ids) >= 2

    @api.depends("duplicated_lead_ids")
    def _compute_merge_duplicates(self):
        """Same rule as the standard ``name`` field, as a plain checkbox."""
        for wizard in self:
            wizard.merge_duplicates = len(wizard.duplicated_lead_ids) >= 2

    def action_apply(self):
        """Drive the standard conversion action from the checkbox.

        Opened on an opportunity there is nothing to convert, so the wizard
        offers merging or not instead of the standard convert/merge choice.
        """
        if self.env.context.get(CUSTOMER_ONLY_CONTEXT):
            for wizard in self:
                wizard.name = (
                    "merge"
                    if wizard.merge_duplicates and wizard.has_duplicates
                    else "convert"
                )
        return super().action_apply()

    def _action_merge(self):
        """Assign the customer of an already converted opportunity.

        The standard implementation only creates the customer when the merge
        result still is a lead, since merging is otherwise reached from the
        conversion of a lead. Opened on an opportunity the customer is the
        whole point, so it has to be handled here.
        """
        result_opportunity = super()._action_merge()
        if (
            self.env.context.get(CUSTOMER_ONLY_CONTEXT)
            and not result_opportunity.partner_id
        ):
            self._convert_handle_partner(
                result_opportunity, self.action, self.partner_id.id
            )
        return result_opportunity
