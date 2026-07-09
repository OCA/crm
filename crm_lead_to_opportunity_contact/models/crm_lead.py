# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _find_contact_in_company(self, company):
        """Return a contact of ``company`` matching the lead's email, if any.

        Matching is done by email, which is the key Odoo itself uses to look up
        partners, and the oldest one wins for the very same reason: it is
        considered the most relevant.
        """
        self.ensure_one()
        if not company or not self.email_normalized:
            return self.env["res.partner"]
        return self.env["res.partner"].search(
            [
                ("parent_id", "=", company.id),
                ("is_company", "=", False),
                ("email_normalized", "=", self.email_normalized),
            ],
            limit=1,
            order="id",
        )
