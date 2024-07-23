# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCrmPartnerContactRole(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create role records
        cls.role_1 = cls.env["res.partner.role"].create({"name": "Role 1"})
        cls.role_2 = cls.env["res.partner.role"].create({"name": "Role 2"})

    def test_create_lead_with_roles(self):
        # Create a lead without partner_id
        lead = self.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "contact_name": "Test Contact",
                "role_ids": [(6, 0, [self.role_1.id, self.role_2.id])],
            }
        )
        # Call _create_customer to create the partner from the lead
        partner = lead._create_customer()
        self.assertTrue(bool(partner), "Partner was not created")
        self.assertEqual(
            partner.role_ids.ids,
            lead.role_ids.ids,
            "Roles do not match between lead and partner",
        )

        # Create a lead with partner_id
        lead = self.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "partner_id": partner.id,
            }
        )
        self.assertEqual(
            lead.role_ids.ids,
            partner.role_ids.ids,
            "Roles do not match between lead and partner",
        )
