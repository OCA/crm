# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    vat = fields.Char(
        string="TIN",
        help="Tax Identification Number. The first 2 characters are the "
        "country code.",
    )

    def _create_customer(self):
        """Add VAT to partner."""
        return super(Lead, self.with_context(default_vat=self.vat))._create_customer()

    def _prepare_values_from_partner(self, partner):
        """Recover VAT from partner if available."""
        result = super(Lead, self)._prepare_values_from_partner(partner)
        if not partner:
            return result
        if partner.vat:
            result["vat"] = partner.vat
        return result
