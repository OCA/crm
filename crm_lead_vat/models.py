# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    vat = fields.Char(
        "TIN",
        help="Tax Identification Number. The first 2 characters are the "
             "country code.")

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Add VAT to partner."""
        return (super(Lead, self.with_context(default_vat=lead.vat))
                ._lead_create_contact(lead, name, is_company, parent_id))

    def on_change_partner_id(self, partner_id):
        """Recover VAT from partner if available."""
        result = super(Lead, self).on_change_partner_id(partner_id)

        if result.get("value"):
            if self.partner_id and self.partner_id.vat:
                result["value"]["vat"] = self.partner_id.vat

        return result
