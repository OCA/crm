# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2021 Doscaal - Alexandre Moreau
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_firstname = fields.Char("First name")
    contact_lastname = fields.Char("Last name")
    contact_name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True,
        readonly=False,
    )

    def _inverse_name(self):
        for record in self:
            parts = self.env['res.partner']._get_inverse_name(
                record.contact_name, False)
            record.contact_lastname = parts["lastname"]
            record.contact_firstname = parts["firstname"]

    def _inverse_name_after_cleaning_whitespace(self):
        for record in self:
            clean = self.env['res.partner']._get_whitespace_cleaned_name(
                record.name)
            record.name = clean
            record._inverse_name()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id.is_company:
            self.contact_firstname = self.partner_id.firstname
            self.contact_lastname = self.partner_id.lastname

    @api.depends("contact_firstname", "contact_lastname")
    def _compute_name(self):
        for record in self:
            record.contact_name = self.env['res.partner']._get_computed_name(
                record.contact_lastname, record.contact_firstname)

    def _prepare_customer_values(self, partner_name, is_company, parent_id=False):
        """Ensure first and last names of contact match those in lead."""
        lead_partner_data = super(CrmLead, self)._prepare_customer_values(
            partner_name, is_company, parent_id
        )
        if not is_company:
            if self.contact_firstname:
                lead_partner_data.update({"firstname": self.contact_firstname})
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
                        "contact_firstname": partner.firstname,
                        "contact_lastname": partner.lastname,
                    }
                )

        return self._convert_to_write(result)

    def _prepare_contact_name_from_partner(self, partner):
        result = super()._prepare_contact_name_from_partner(partner)
        contact_firstname = False if partner.is_company else partner.firstname
        contact_lastname = False if partner.is_company else partner.lastname
        result.update(
            {
                "contact_firstname": contact_firstname or self.contact_firstname,
                "contact_lastname": contact_lastname or self.contact_lastname,
            }
        )
        return result
