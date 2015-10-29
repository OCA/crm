# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from .. import exceptions as ex


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

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Add invoice address to partner."""
        result = (super(Lead, self)
                  ._lead_create_contact(lead, name, is_company, parent_id))

        partner = self.env["res.partner"].browse(result)
        if not lead.invoice_equal:
            if not (lead.contact_name and lead.partner_name):
                raise ex.Need2PartnersError()

            elif parent_id:
                partner.parent_id.update({
                    "type": "invoice",
                    "street": lead.invoice_street,
                    "street2": lead.invoice_street2,
                    "zip": lead.invoice_zip,
                    "city": lead.invoice_city,
                    "state_id": (lead.invoice_state_id and
                                 lead.invoice_state_id.id),
                    "country_id": (lead.invoice_country_id and
                                   lead.invoice_country_id.id),
                })

        return result

    @api.multi
    @api.onchange("invoice_state_id")
    def _invoice_state_id_change(self):
        """Update country in UI."""
        if self.invoice_state_id:
            self.invoice_country_id = self.invoice_state_id.country_id
