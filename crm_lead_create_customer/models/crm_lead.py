# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.exceptions import UserError

from ..wizard.crm_lead2opportunity_partner import CUSTOMER_ONLY_CONTEXT


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def action_create_customer(self):
        """Open the standard conversion wizard to build the customer.

        Standard CRM only reaches that wizard from a lead, so an opportunity
        that never was one, such as the ones the website contact form creates
        when the sales team does not use leads, keeps its contact details
        denormalized and never gets a customer. The wizard itself needs no
        change: it already lets the user create the customer or link an
        existing one, and offers to merge the duplicates it detects.
        """
        self.ensure_one()
        if self.partner_id:
            raise UserError(
                self.env._("%s already has a customer assigned.", self.display_name)
            )
        if not (self.contact_name or self.partner_name or self.email_from):
            raise UserError(
                self.env._(
                    "Fill in the contact name, the company name or the email "
                    "before creating the customer, otherwise the customer "
                    "would be named after the %s subject.",
                    self.display_name,
                )
            )
        action = self.env["ir.actions.actions"]._for_xml_id(
            "crm_lead_create_customer.crm_lead_customer_create_action"
        )
        action["context"] = {
            "active_model": self._name,
            "active_id": self.id,
            "active_ids": self.ids,
            CUSTOMER_ONLY_CONTEXT: True,
        }
        return action
