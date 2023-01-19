# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _create_child_partner(self, parent_partner_id):
        self.ensure_one()
        assert parent_partner_id
        rpo = self.env["res.partner"]
        contact_name = self.contact_name
        if not contact_name and self.email_from:
            contact_name = rpo._parse_partner_name(self.email_from)[0]
        if not contact_name:
            raise UserError(
                _("Contact name is not set on lead '%s'.") % self.display_name
            )
        vals = self.with_context(
            default_user_id=self.user_id.id
        )._prepare_customer_values(
            contact_name,
            is_company=False,
            parent_id=parent_partner_id,
        )
        partner = rpo.create(vals)
        return partner
