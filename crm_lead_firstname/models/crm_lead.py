# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import OrderedDict
from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_name = fields.Char("First name")
    contact_lastname = fields.Char("Last name")

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Ensure first and last names of contact match those in lead."""
        partner_id = super(CrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id)
        if not is_company and partner_id:
            partner = self.env["res.partner"].browse(partner_id)

            # Write fields with values first
            partner.update(
                OrderedDict(
                    sorted(
                        (("firstname", lead.contact_name),
                         ("lastname", lead.contact_lastname)),
                        key=lambda item: item[1],
                        reverse=True)))
        return partner_id

    @api.multi
    def on_change_partner_id(self, partner_id):
        """Recover first and last names from partner if available."""
        result = super(CrmLead, self).on_change_partner_id(partner_id)

        if result.get("value") and partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if not partner.is_company:
                result["value"].update({
                    "contact_name": partner.firstname,
                    "contact_lastname": partner.lastname,
                })

        return result
