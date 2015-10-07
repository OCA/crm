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

    @api.returns("res.partner")
    def _lead_create_contact(self, *args, **kwargs):
        """Add trade name to partner."""
        self.ensure_one()
        return (super(Lead, self.with_context(default_customer=self.customer,
                                              default_supplier=self.supplier))
                ._lead_create_contact(*args, **kwargs))

    def on_change_partner_id(self, partner_id):
        """Recover customer and supplier from partner if available."""
        result = super(Lead, self).on_change_partner_id(partner_id)

        if result.get("value"):
            partner = self.pool.get("res.partner").browse(partner_id)
            if partner:
                result["value"]["customer"] = partner.customer
                result["value"]["supplier"] = partner.supplier

        return result
