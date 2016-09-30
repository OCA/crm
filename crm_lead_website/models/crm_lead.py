# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    website = fields.Char()

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Add trade name to partner."""
        return (super(CrmLead, self.with_context(default_website=lead.website))
                ._lead_create_contact(lead, name, is_company, parent_id))

    @api.multi
    def on_change_partner_id(self, partner_id):
        """Recover website from partner if available."""
        result = super(CrmLead, self).on_change_partner_id(partner_id)

        if result.get("value") and partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if partner.website:
                result["value"]["website"] = partner.website

        return result
