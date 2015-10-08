# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    invoice_equal = fields.Boolean(
        "Use same adress for billing",
        default=True,
        help="Uncheck this option to specify a different billing address.")
    invoice_street = fields.Char("Invoice address street")
    invoice_street2 = fields.Char("Invoice address street 2")
    invoice_city = fields.Char("Invoice address city")
    invoice_state_id = fields.Many2one("res.country.state",
                                       "Invoice address state")
    invoice_zip = fields.Char("Invoice address ZIP code")
    invoice_country_id = fields.Many2one("res.country",
                                         "Invoice address country")

    @api.returns("res.partner")
    def _lead_create_contact(self, name, is_company, *args, **kwargs):
        """Add invoice address to partner."""
        self.ensure_one()
        result = (super(Lead, self)
                  ._lead_create_contact(name, is_company, *args, **kwargs))

        if is_company and not self.invoice_equal:
            result.update({
                "type": "invoice",
                "street": self.invoice_street or result.get("street"),
                "street2": self.invoice_street2 or result.get("street2"),
                "zip": self.invoice_zip or result.get("zip"),
                "city": self.invoice_city or result.get("city"),
                "state_id": (self.invoice_state_id and
                             self.invoice_state_id.id or
                             result.get("state_id")),
                "country_id": (self.invoice_country_id and
                               self.invoice_country_id.id or
                               result.get("country_id")),
            })

        return result

    @api.onchange("invoice_state_id")
    def _invoice_state_id_change(self):
        """Update country in UI."""
        self.ensure_one()
        if self.invoice_state_id:
            self.invoice_country_id = self.invoice_state_id.country_id
