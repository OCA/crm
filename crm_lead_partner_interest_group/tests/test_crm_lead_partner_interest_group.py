# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase


class TestCrmLeadPartnerInterestGroup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        InterestGroup = cls.env["res.partner.interest.group"]
        cls.group_a = InterestGroup.create({"name": "Group A"})
        cls.group_b = InterestGroup.create({"name": "Group B"})

    def _new_lead_form(self):
        return Form(self.env["crm.lead"])

    def test_lead_interest_group_field(self):
        lead_form = self._new_lead_form()
        lead_form.name = "Lead with interests"
        lead_form.contact_name = "Test Contact"
        lead_form.email_from = "test.contact@example.com"
        lead_form.interest_group_ids.add(self.group_a)
        lead_form.interest_group_ids.add(self.group_b)
        lead = lead_form.save()
        self.assertEqual(lead.interest_group_ids, self.group_a + self.group_b)

    def test_create_partner_from_lead_propagates_interest_groups(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead generating partner",
                "contact_name": "John Doe",
                "email_from": "john.doe@example.com",
                "interest_group_ids": [(6, 0, (self.group_a + self.group_b).ids)],
            }
        )
        self.assertFalse(lead.partner_id)
        lead._handle_partner_assignment()
        self.assertTrue(lead.partner_id)
        self.assertEqual(
            lead.partner_id.interest_group_ids,
            self.group_a + self.group_b,
        )

    def test_create_partner_from_lead_without_interest_groups(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead without interests",
                "contact_name": "Jane Doe",
                "email_from": "jane.doe@example.com",
            }
        )
        lead._handle_partner_assignment()
        self.assertTrue(lead.partner_id)
        self.assertFalse(lead.partner_id.interest_group_ids)

    def test_partner_creation_with_company(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead with company",
                "contact_name": "Foo Contact",
                "partner_name": "ACME Inc.",
                "email_from": "contact@acme.example.com",
                "interest_group_ids": [(6, 0, self.group_a.ids)],
            }
        )
        lead._handle_partner_assignment()
        partner = lead.partner_id
        self.assertTrue(partner)
        self.assertEqual(partner.interest_group_ids, self.group_a)
        # The parent company partner should NOT carry interest groups,
        # as those belong to the individual contact only.
        self.assertTrue(partner.parent_id)
        self.assertFalse(partner.parent_id.interest_group_ids)
