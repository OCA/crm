# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_name = fields.Char("First name")
    contact_lastname = fields.Char("Last name")

    def _prepare_customer_values(self, partner_name, is_company, parent_id=False):
        """Ensure first and last names of contact match those in lead."""
        lead_partner_data = super(CrmLead, self)._prepare_customer_values(
            partner_name, is_company, parent_id
        )
        if not is_company:
            if self.contact_name:
                lead_partner_data.update({"firstname": self.contact_name})
                if "name" in lead_partner_data:
                    del lead_partner_data["name"]
            if self.contact_lastname:
                lead_partner_data.update({"lastname": self.contact_lastname})
                if "name" in lead_partner_data:
                    del lead_partner_data["name"]
        return lead_partner_data

    def _prepare_values_from_partner(self, partner):
        """Recover first and last names from partner if available."""
        result = super(CrmLead, self)._prepare_values_from_partner(partner)

        if partner:
            if not partner.is_company:
                result.update(
                    {
                        "contact_name": partner.firstname,
                        "contact_lastname": partner.lastname,
                    }
                )

        return self._convert_to_write(result)

    def _prepare_contact_name_from_partner(self, partner):
        result = super()._prepare_contact_name_from_partner(partner)
        contact_name = False if partner.is_company else partner.firstname
        contact_lastname = False if partner.is_company else partner.lastname
        result.update(
            {
                "contact_name": contact_name or self.contact_name,
                "contact_lastname": contact_lastname or self.contact_lastname,
            }
        )
        return result
