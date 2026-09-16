# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class CrmLead2OpportunityPartner(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"

    # When linking to an existing company, this sub-question decides what
    # happens to the lead's contact.
    contact_action = fields.Selection(
        selection=[
            ("create_contact", "Create a new contact"),
            ("link_contact", "Link to an existing contact"),
            ("no_contact", "Do not add a contact"),
        ],
        compute="_compute_contact",
        store=True,
        readonly=False,
    )
    contact_partner_id = fields.Many2one(
        "res.partner",
        string="Contact",
        compute="_compute_contact",
        store=True,
        readonly=False,
    )
    # Only a company can be given a contact: when the selected customer is a
    # person, the sub-question makes no sense and is not asked.
    partner_is_company = fields.Boolean(related="partner_id.is_company")

    @api.depends("action", "lead_id", "partner_id.is_company")
    def _compute_contact(self):
        """Default the contact sub-question: if a contact of the selected
        company already matches the lead (by email), pre-select it and default
        to 'link'; otherwise default to 'create'."""
        for wiz in self:
            match = wiz.env["res.partner"]
            if wiz.action == "exist" and wiz.partner_is_company and wiz.lead_id:
                match = wiz.lead_id._find_contact_in_company(wiz.partner_id)
            wiz.contact_partner_id = match
            wiz.contact_action = "link_contact" if match else "create_contact"

    def _contact_action_applies(self, lead):
        """Whether the contact sub-question was actually asked to the user.

        It is only asked when converting (the "merge" mode hides the customer
        question altogether), onto a selected existing customer that is a
        company, and for a lead that has a contact name. In every other case the
        native behaviour is kept: link the selected customer only.
        """
        self.ensure_one()
        return bool(
            self.name == "convert" and self.partner_is_company and lead.contact_name
        )

    def _check_contact_partner(self):
        """Validate the selected contact server side.

        The view already restricts ``contact_partner_id`` to the active contacts
        of the selected company, but that domain is not enforced on other write
        paths (RPC, data imports), so the same rules are checked here.
        """
        self.ensure_one()
        contact = self.contact_partner_id
        if not contact:
            raise UserError(self.env._("You must select a Contact."))
        if contact.is_company or contact.parent_id != self.partner_id:
            raise UserError(
                self.env._(
                    "The contact %(contact)s is not a contact of %(customer)s.",
                    contact=contact.display_name,
                    customer=self.partner_id.display_name,
                )
            )
        if not contact.active:
            raise UserError(
                self.env._(
                    "The contact %(contact)s is archived.",
                    contact=contact.display_name,
                )
            )

    def _convert_handle_partner(self, lead, action, partner_id):
        if action == "exist" and self._contact_action_applies(lead):
            if self.contact_action == "create_contact":
                # ``_create_customer`` attaches the new contact to ``with_parent``
                # instead of creating a company out of the lead's company name,
                # and propagates the salesperson through ``default_user_id``,
                # exactly like the native conversion does.
                partner = lead.with_context(
                    default_user_id=self.user_id.id
                )._create_customer(with_parent=self.partner_id)
                lead.write({"partner_id": partner.id})
                return
            if self.contact_action == "link_contact":
                self._check_contact_partner()
                lead.write({"partner_id": self.contact_partner_id.id})
                return
        return super()._convert_handle_partner(lead, action, partner_id)


class CrmLead2OpportunityPartnerMass(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner.mass"

    def _contact_action_applies(self, lead):
        """The mass conversion wizard never asks the contact sub-question, so it
        must never apply it: every lead keeps the native behaviour."""
        return False
