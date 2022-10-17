# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Opportunity2Rfq(models.TransientModel):
    _name = "srm.rfq.partner"
    _description = "Create new or use existing Supplier on new RFQ"

    @api.model
    def default_get(self, fields):
        result = super(Opportunity2Rfq, self).default_get(fields)

        active_model = self._context.get("active_model")
        if active_model != "crm.lead":
            raise UserError(_("You can only apply this action from a lead."))

        lead = False
        if result.get("lead_id"):
            lead = self.env["crm.lead"].browse(result["lead_id"])
        elif "lead_id" in fields and self._context.get("active_id"):
            lead = self.env["crm.lead"].browse(self._context["active_id"])
        if lead:
            result["lead_id"] = lead.id
            partner_id = result.get("partner_id") or lead._find_matching_partner().id
            if "action" in fields and not result.get("action"):
                result["action"] = "exist" if partner_id else "create"
            if "partner_id" in fields and not result.get("partner_id"):
                result["partner_id"] = partner_id

        return result

    action = fields.Selection(
        [
            ("create", "Create a new vendor"),
            ("exist", "Link to an existing vendor"),
            ("nothing", "Do not link to a vendor"),
        ],
        string="RFQ Vendor",
        required=True,
    )
    lead_id = fields.Many2one("crm.lead", "Associated Lead", required=True)
    partner_id = fields.Many2one("res.partner", "Vendor")

    def action_apply(self):
        """Convert lead to opportunity or merge lead and opportunity and open
        the freshly created opportunity view.
        """
        self.ensure_one()
        if self.action == "create":
            self.lead_id.handle_partner_assignment(create_missing=True)
        elif self.action == "exist":
            self.lead_id.handle_partner_assignment(
                force_partner_id=self.partner_id.id, create_missing=False
            )
        return self.lead_id.action_rfq_new()
