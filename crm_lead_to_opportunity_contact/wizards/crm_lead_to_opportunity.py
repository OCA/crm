# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class CrmLead2OpportunityPartner(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"

    action = fields.Selection(
        selection_add=[
            ("create_child", "Create a new contact on an existing customer")
        ],
        ondelete={"create_child": "set null"},
    )
    # I don't re-use the native field 'partner_id' because I need a specific domain
    create_child_partner_id = fields.Many2one(
        "res.partner", string="Existing Customer", domain=[("parent_id", "=", False)]
    )

    def _convert_handle_partner(self, lead, action, partner_id):
        if action == "create_child":
            if not self.create_child_partner_id:
                raise UserError(_("You must select an Existing Customer."))
            partner = lead._create_child_partner(self.create_child_partner_id.id)
            lead.write({"partner_id": partner.id})
        else:
            return super()._convert_handle_partner(lead, action, partner_id)
