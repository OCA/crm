# Copyright 2023 Akretion France (http://www.akretion.com/)
# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestCrmLeadToOpportunityContact(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.partner"].create(
            {"name": "Test Company", "is_company": True}
        )
        cls.contact = cls.env["res.partner"].create(
            {
                "name": "Existing Peter",
                "parent_id": cls.company.id,
                "email": "peter@example.com",
            }
        )

    def _make_lead(self, **kw):
        return self.env["crm.lead"].create({"name": "Test Lead", "type": "lead", **kw})

    def _wizard(self, lead, **vals):
        return (
            self.env["crm.lead2opportunity.partner"]
            .with_context(
                active_model="crm.lead", active_id=lead.id, active_ids=lead.ids
            )
            .create({"name": "convert", **vals})
        )

    def _convert(self, lead, **vals):
        self._wizard(lead, **vals).action_apply()
        return lead

    # ------------------------------------------------------------------ create
    def test_create_contact(self):
        """A new contact is created under the company and assigned to the opp."""
        lead = self._make_lead(contact_name="John Doe", email_from="john@example.com")
        self._convert(
            lead,
            action="exist",
            partner_id=self.company.id,
            contact_action="create_contact",
        )
        partner = lead.partner_id
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.parent_id, self.company)
        self.assertEqual(partner.name, "John Doe")

    def test_create_contact_does_not_duplicate_the_company(self):
        """A lead carrying a company name must not create a second company.

        This is what the native wizard cannot do: with a company name on the
        lead it either creates a duplicate company, or drops the contact.
        """
        lead = self._make_lead(
            contact_name="John Doe",
            email_from="john@example.com",
            partner_name=self.company.name,
        )
        companies = self.env["res.partner"].search_count([("is_company", "=", True)])
        self._convert(
            lead,
            action="exist",
            partner_id=self.company.id,
            contact_action="create_contact",
        )
        self.assertEqual(lead.partner_id.parent_id, self.company)
        self.assertEqual(
            self.env["res.partner"].search_count([("is_company", "=", True)]),
            companies,
        )

    # -------------------------------------------------------------------- link
    def test_link_contact(self):
        """The opportunity is assigned to the selected existing contact."""
        lead = self._make_lead(contact_name="Whatever", email_from="x@example.com")
        self._convert(
            lead,
            action="exist",
            partner_id=self.company.id,
            contact_action="link_contact",
            contact_partner_id=self.contact.id,
        )
        self.assertEqual(lead.partner_id, self.contact)

    def test_link_contact_requires_a_contact(self):
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        with self.assertRaises(UserError):
            self._convert(
                lead,
                action="exist",
                partner_id=self.company.id,
                contact_action="link_contact",
            )

    # --------------------------------------------------------------- no contact
    def test_no_contact_keeps_the_company(self):
        """'Do not add a contact' keeps the native behaviour: link the company."""
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        count = self.env["res.partner"].search_count([])
        self._convert(
            lead,
            action="exist",
            partner_id=self.company.id,
            contact_action="no_contact",
        )
        self.assertEqual(lead.partner_id, self.company)
        self.assertEqual(self.env["res.partner"].search_count([]), count)

    def test_without_contact_name_keeps_the_company(self):
        """Without a contact name the sub-question does not apply (native).

        The email carries a name on purpose: without the ``contact_name`` gate
        the native ``_create_customer`` would parse it and create a contact.
        """
        lead = self._make_lead(email_from="Jane Roe <jane@example.com>")
        count = self.env["res.partner"].search_count([])
        self._convert(lead, action="exist", partner_id=self.company.id)
        self.assertEqual(lead.partner_id, self.company)
        self.assertEqual(self.env["res.partner"].search_count([]), count)

    # ----------------------------------------------------------- smart default
    def test_smart_default_matches_by_email(self):
        """A contact of the company matching the lead email is pre-selected."""
        lead = self._make_lead(contact_name="Peter", email_from="peter@example.com")
        wizard = self._wizard(lead, action="exist", partner_id=self.company.id)
        self.assertEqual(wizard.contact_action, "link_contact")
        self.assertEqual(wizard.contact_partner_id, self.contact)

    def test_smart_default_matches_a_malformed_email(self):
        """An email that cannot be normalized is compared as it was typed.

        Odoo keys partners on the normalized email and falls back to the raw
        input when normalization fails, so the customer lookup matches such
        leads; the contact lookup must not be stricter.
        """
        broken = self.env["res.partner"].create(
            {
                "name": "Typo Peter",
                "parent_id": self.company.id,
                "email": "peter.example.com",
            }
        )
        self.assertFalse(broken.email_normalized)
        lead = self._make_lead(contact_name="Peter", email_from="peter.example.com")
        wizard = self._wizard(lead, action="exist", partner_id=self.company.id)
        self.assertEqual(wizard.contact_action, "link_contact")
        self.assertEqual(wizard.contact_partner_id, broken)

    def test_smart_default_without_match(self):
        lead = self._make_lead(contact_name="New", email_from="new@example.com")
        wizard = self._wizard(lead, action="exist", partner_id=self.company.id)
        self.assertEqual(wizard.contact_action, "create_contact")
        self.assertFalse(wizard.contact_partner_id)

    # -------------------------------------------------------------------- merge
    def test_merge_does_not_apply_the_contact_sub_question(self):
        """In 'merge' mode the sub-question is not asked, so it must not apply."""
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        duplicate = self._make_lead(contact_name="John", email_from="john@example.com")
        count = self.env["res.partner"].search_count([])
        wizard = self._wizard(
            lead,
            name="merge",
            action="exist",
            partner_id=self.company.id,
            contact_action="create_contact",
            duplicated_lead_ids=[(6, 0, duplicate.ids)],
        )
        wizard.action_apply()
        # native behaviour: the company is linked, no contact is created
        self.assertEqual(self.env["res.partner"].search_count([]), count)
        self.assertEqual(wizard.lead_id.partner_id, self.company)

    # --------------------------------------------------------------------- mass
    def test_mass_convert_does_not_apply_the_contact_sub_question(self):
        """The mass wizard does not ask the sub-question, so it must not apply it."""
        leads = self.env["crm.lead"].create(
            [
                {
                    "name": f"Mass {i}",
                    "type": "lead",
                    "contact_name": f"Mass Contact {i}",
                    "email_from": f"mass{i}@example.com",
                }
                for i in range(3)
            ]
        )
        count = self.env["res.partner"].search_count([])
        wizard = (
            self.env["crm.lead2opportunity.partner.mass"]
            .with_context(
                active_model="crm.lead", active_ids=leads.ids, active_id=leads[0].id
            )
            .create({"action": "exist", "partner_id": self.company.id})
        )
        wizard.action_mass_convert()
        # native behaviour: every lead is linked to the company, nothing created
        self.assertEqual(self.env["res.partner"].search_count([]), count)
        self.assertEqual(leads.mapped("partner_id"), self.company)

    # -------------------------------------------------------------- robustness
    def test_without_a_customer_falls_back_to_native(self):
        """action='exist' without a customer must not crash (native fallback)."""
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        count = self.env["res.partner"].search_count([])
        wizard = self._wizard(
            lead, action="exist", contact_action="create_contact", partner_id=False
        )
        wizard.action_apply()
        self.assertEqual(self.env["res.partner"].search_count([]), count)

    def test_a_person_customer_falls_back_to_native(self):
        """A contact cannot be added to a person: keep the native behaviour."""
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        count = self.env["res.partner"].search_count([])
        self._convert(
            lead,
            action="exist",
            partner_id=self.contact.id,  # a person, not a company
            contact_action="create_contact",
        )
        self.assertEqual(lead.partner_id, self.contact)
        self.assertEqual(self.env["res.partner"].search_count([]), count)

    def test_link_contact_of_another_company_is_rejected(self):
        """The view domain is enforced server side too."""
        other_company = self.env["res.partner"].create(
            {"name": "Other Company", "is_company": True}
        )
        alien = self.env["res.partner"].create(
            {"name": "Alien", "parent_id": other_company.id}
        )
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        with self.assertRaises(UserError):
            self._convert(
                lead,
                action="exist",
                partner_id=self.company.id,
                contact_action="link_contact",
                contact_partner_id=alien.id,
            )

    def test_link_an_archived_contact_is_rejected(self):
        """The view never offers archived contacts: enforce it server side."""
        self.contact.action_archive()
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        with self.assertRaises(UserError):
            self._convert(
                lead,
                action="exist",
                partner_id=self.company.id,
                contact_action="link_contact",
                contact_partner_id=self.contact.id,
            )

    def test_created_contact_gets_the_wizard_salesperson(self):
        """The salesperson chosen in the wizard wins over the lead's one."""
        lead_user = self.env["res.users"].create(
            {"name": "Lead Salesperson", "login": "l2o_contact_lead_user"}
        )
        wizard_user = self.env.user
        lead = self._make_lead(
            contact_name="John", email_from="john@example.com", user_id=lead_user.id
        )
        self._convert(
            lead,
            action="exist",
            partner_id=self.company.id,
            contact_action="create_contact",
            user_id=wizard_user.id,
        )
        self.assertEqual(lead.partner_id.user_id, wizard_user)

    def test_link_a_company_as_contact_is_rejected(self):
        """The contact must be a person, never a company."""
        sub_company = self.env["res.partner"].create(
            {"name": "Sub Company", "parent_id": self.company.id, "is_company": True}
        )
        lead = self._make_lead(contact_name="John", email_from="john@example.com")
        with self.assertRaises(UserError):
            self._convert(
                lead,
                action="exist",
                partner_id=self.company.id,
                contact_action="link_contact",
                contact_partner_id=sub_company.id,
            )

    # ----------------------------------------------------------- smart default
    def test_smart_default_picks_the_oldest_contact(self):
        """Like Odoo does, the oldest matching partner wins over the others."""
        oldest = self.env["res.partner"].create(
            {"name": "Zoe", "parent_id": self.company.id, "email": "dup@example.com"}
        )
        self.env["res.partner"].create(
            {"name": "Ana", "parent_id": self.company.id, "email": "dup@example.com"}
        )
        lead = self._make_lead(contact_name="Dup", email_from="dup@example.com")
        wizard = self._wizard(lead, action="exist", partner_id=self.company.id)
        # "Ana" comes first alphabetically, which is res.partner's default order
        self.assertEqual(wizard.contact_partner_id, oldest)

    # -------------------------------------------------------------- native path
    def test_native_create_customer_still_works(self):
        lead = self._make_lead(
            contact_name="Bob", partner_name="NewCo", email_from="bob@newco.com"
        )
        self._convert(lead, action="create")
        partner = lead.partner_id
        self.assertEqual(partner.name, "Bob")
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.parent_id.name, "NewCo")
        self.assertTrue(partner.parent_id.is_company)
