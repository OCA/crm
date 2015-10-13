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

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        """Recover VAT from partner if available."""
        result = super(Lead, self).on_change_partner_id(
            cr, uid, ids, partner_id, context=context)

        if result.get("value"):
            partner = self.pool.get("res.partner").browse(
                cr, uid, partner_id, context=context)
            if partner.vat:
                result["value"]["vat"] = partner.vat

        return result
