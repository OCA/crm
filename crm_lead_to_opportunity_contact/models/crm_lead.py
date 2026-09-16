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

        As in ``MailThread._partner_find_from_emails()``, the normalized email
        is the key, unless it is wrong and cannot be normalized, in which case
        the raw input is compared instead. That keeps this lookup consistent
        with the one filling the customer, which goes through that tool.
        """
        self.ensure_one()
        email = self.email_normalized or self.email_from
        if not company or not email:
            return self.env["res.partner"]
        email_domain = (
            [("email_normalized", "=", email)]
            if self.email_normalized
            else [("email", "=", email)]
        )
        return self.env["res.partner"].search(
            [
                ("parent_id", "=", company.id),
                ("is_company", "=", False),
            ]
            + email_domain,
            limit=1,
            order="id",
        )
