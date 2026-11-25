# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _vat_search_variants(self, vat):
        """Return the VAT spellings to look for.

        ``res.partner.vat`` is free text: neither ``base`` nor ``base_vat``
        normalizes it on write, so it is stored exactly as it was typed. The
        value as typed is therefore searched alongside the normalized one, and
        the case is never altered, so that a partner whose VAT was stored
        verbatim is found too.
        """
        # Sometimes the VAT is typed with whitespaces or dots.
        return (vat.replace(" ", "").replace(".", ""), vat)

    def _find_company_by_vat(self):
        """Return the company matching the lead's VAT (TIN), if any.

        Exact matches are used on purpose (not ``=ilike``): the VAT is free
        text, so wildcard characters must be compared literally, and equality
        hits the index on ``res.partner.vat``.
        """
        self.ensure_one()
        if not self.vat:
            return self.env["res.partner"]
        return self.env["res.partner"].search(
            [
                ("is_company", "=", True),
                ("vat", "in", self._vat_search_variants(self.vat)),
            ],
            limit=1,
            order="id",
        )

    def _find_matching_partner(self):
        """Prefer the company matched by the lead's VAT, falling back to the
        native email lookup when the lead has no VAT or no company carries it.
        """
        self.ensure_one()
        return self._find_company_by_vat() or super()._find_matching_partner()
