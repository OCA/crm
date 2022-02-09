from odoo.tests.common import SingleTransactionCase


class CrmNACECase(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.nace_0 = cls.env["res.partner.nace"].create(
            {"name": "name_0", "code": "code_0"}
        )
        cls.nace_1 = cls.env["res.partner.nace"].create(
            {"name": "name_1", "code": "code_1"}
        )
        cls.nace_2 = cls.env["res.partner.nace"].create(
            {"name": "name_2", "code": "code_2"}
        )

    def test_data_transferred_to_partner(self):
        """Data is moved to partner when creating it from lead."""
        # Create a lead with nace codes but without partner yet
        lead = self.env["crm.lead"].create(
            {
                "name": "test lead",
                "partner_name": "someone",
                "nace_id": self.nace_0.id,
                "secondary_nace_ids": [(4, self.nace_1.id), (4, self.nace_2.id)],
            }
        )
        self.assertFalse(lead.partner_id)
        # Create that partner automatically
        partner = lead._create_customer()
        self.assertEqual(partner.nace_id, self.nace_0)
        self.assertEqual(partner.secondary_nace_ids, self.nace_1 | self.nace_2)
