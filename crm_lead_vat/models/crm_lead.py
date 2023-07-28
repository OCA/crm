# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    vat = fields.Char(
        string="TIN",
        help="Tax Identification Number. The first 2 characters are the "
        "country code.",
        compute="_compute_vat",
        inverse="_inverse_vat",
        readonly=False,
        store=True,
    )
    partner_vat_update = fields.Boolean(
        "Partner VAT will Update", compute="_compute_partner_vat_update"
    )

    @api.depends("partner_id.vat", "partner_id.commercial_partner_id.vat")
    def _compute_vat(self):
        for lead in self:
            if (
                lead.partner_id.commercial_partner_id.vat
                and lead._get_partner_vat_update()
            ):
                lead.vat = lead.partner_id.commercial_partner_id.vat
            elif lead.partner_id.vat and lead._get_partner_vat_update():
                lead.vat = lead.partner_id.vat

    def _inverse_vat(self):
        for lead in self:
            if lead._get_partner_vat_update():
                if lead.partner_id.commercial_partner_id:
                    lead.partner_id.commercial_partner_id.vat = lead.vat
                else:
                    lead.partner_id.vat = lead.vat

    @api.depends("vat", "partner_id")
    def _compute_partner_vat_update(self):
        for lead in self:
            lead.partner_vat_update = lead._get_partner_vat_update()

    def _get_partner_vat_update(self):
        """Calculate if we should write the vat on the related partner. When
        the vat of the lead / partner is an empty string, we force it to False
        to not propagate a False on an empty string.

        Done in a separate method so it can be used in both ribbon and inverse
        and compute of vat update methods.
        """
        self.ensure_one()
        if (
            self.partner_id.commercial_partner_id
            and self.vat != self.partner_id.commercial_partner_id.vat
        ):
            return self.vat != self.partner_id.commercial_partner_id.vat
        elif self.partner_id and self.vat != self.partner_id.vat:
            return self.vat != self.partner_id.vat
        return False

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """Add VAT to partner."""
        res = super(Lead, self)._prepare_customer_values(
            partner_name, is_company, parent_id
        )
        res.update(
            {
                "vat": self.vat,
            }
        )
        return res

    def _prepare_values_from_partner(self, partner):
        """Recover VAT from partner if available."""
        result = super(Lead, self)._prepare_values_from_partner(partner)
        if not partner:
            return result
        if partner.vat:
            result["vat"] = partner.vat
        return result
