# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal - Tecnativa S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    website = fields.Char()

    @api.model
    def _lead_create_contact(self, name, is_company, parent_id=False):
        """Add trade name to partner."""
        return (super(CrmLead,
                      self.with_context(default_website=self.website)
                      )._lead_create_contact(name, is_company, parent_id))

    @api.multi
    def _onchange_partner_id_values(self, partner_id):
        """Recover website from partner if available."""
        result = super(CrmLead, self)._onchange_partner_id_values(partner_id)
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if partner.website:
                result.update({"website": partner.website})
        return result
