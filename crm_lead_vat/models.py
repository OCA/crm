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

    @api.one
    def _map_values_to_partner(self, *args, **kwargs):
        """Add VAT to mapped values."""
        result = super(Lead, self)._map_values_to_partner(*args, **kwargs)[0]
        result["vat"] = self.vat
        return result

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
