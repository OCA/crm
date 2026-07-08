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

    def _make_lead(self, **kw):
        vals = {"name": "Test Lead", "type": "lead"}
        vals.update(kw)
        return self.env["crm.lead"].create(vals)

    def _convert(self, lead, **wiz_vals):
        wizard = (
            self.env["crm.lead2opportunity.partner"]
            .with_context(
                active_model="crm.lead", active_id=lead.id, active_ids=lead.ids
            )
            .create({"name": "convert", **wiz_vals})
        )
        wizard.action_apply()
        return lead

    def test_create_child_contact(self):
        """A new contact is created under the existing company and the
        opportunity is assigned to that contact (not the company)."""
        lead = self._make_lead(
            contact_name="John Doe",
            partner_name="Ignored Co",
            email_from="john@example.com",
        )
        self._convert(
            lead, action="create_child", create_child_partner_id=self.company.id
        )
        partner = lead.partner_id
        self.assertTrue(partner)
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.parent_id, self.company)
        self.assertEqual(partner.name, "John Doe")

    def test_contact_name_from_email(self):
        """When the lead has no contact name, it is parsed from the email."""
        lead = self._make_lead(
            contact_name=False, email_from="Jane Roe <jane@example.com>"
        )
        self._convert(
            lead, action="create_child", create_child_partner_id=self.company.id
        )
        self.assertEqual(lead.partner_id.parent_id, self.company)
        self.assertEqual(lead.partner_id.name, "Jane Roe")

    def test_error_without_existing_customer(self):
        """An existing customer must be selected for the new option."""
        lead = self._make_lead(contact_name="John Doe", email_from="john@example.com")
        with self.assertRaises(UserError):
            self._convert(lead, action="create_child")

    def test_error_without_contact_name(self):
        """A contact name (or email to parse it from) is required."""
        lead = self._make_lead(contact_name=False, email_from=False)
        with self.assertRaises(UserError):
            self._convert(
                lead, action="create_child", create_child_partner_id=self.company.id
            )

    def test_native_action_still_works(self):
        """The native 'link to existing customer' option is not broken."""
        lead = self._make_lead(
            contact_name="Bob", partner_name="Y", email_from="bob@example.com"
        )
        self._convert(lead, action="exist", partner_id=self.company.id)
        self.assertEqual(lead.partner_id, self.company)
