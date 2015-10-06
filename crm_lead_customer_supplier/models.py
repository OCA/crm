# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    customer = fields.Boolean(
        help="Check this box if this contact is a customer.")
    supplier = fields.Boolean(
        help="Check this box if this contact is a supplier.")

    @api.one
    def _map_values_to_partner(self, *args, **kwargs):
        """Add customer and supplier to mapped values."""
        result = super(Lead, self)._map_values_to_partner(*args, **kwargs)[0]
        result["customer"] = self.customer
        result["supplier"] = self.supplier
        return result

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        """Recover customer and supplier from partner if available."""
        result = super(Lead, self).on_change_partner_id(
            cr, uid, ids, partner_id, context=context)

        if result.get("value"):
            partner = self.pool.get("res.partner").browse(
                cr, uid, partner_id, context=context)
            if partner:
                result["value"]["customer"] = partner.customer
                result["value"]["supplier"] = partner.supplier

        return result
