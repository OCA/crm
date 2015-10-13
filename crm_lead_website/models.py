# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    website = fields.Char()

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Add trade name to partner."""
        return (super(Lead, self.with_context(default_website=lead.website))
                ._lead_create_contact(lead, name, is_company, parent_id))

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        """Recover website from partner if available."""
        result = super(Lead, self).on_change_partner_id(
            cr, uid, ids, partner_id, context=context)

        if result.get("value"):
            partner = self.pool.get("res.partner").browse(
                cr, uid, partner_id, context=context)
            if partner.website:
                result["value"]["website"] = partner.website

        return result
