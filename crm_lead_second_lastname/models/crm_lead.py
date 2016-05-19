# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import OrderedDict
from openerp.addons.crm_lead_firstname.models.crm_lead \
    import CrmLead as FirstnameCrmLead
from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_lastname2 = fields.Char("Second last name")

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Ensure first and last names of contact match those in lead."""
        # Skip method from :mod:`crm_lead_firstname`
        partner_id = super(FirstnameCrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id)
        if not is_company and partner_id:
            partner = self.env["res.partner"].browse(partner_id)

            # Write fields with values first
            partner.update(
                OrderedDict(
                    sorted(
                        (("firstname", lead.contact_name),
                         ("lastname", lead.contact_lastname),
                         ("lastname2", lead.contact_lastname2)),
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
                    "contact_lastname2": partner.lastname2,
                })

        return result
