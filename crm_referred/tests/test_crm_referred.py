# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.tests.common import TransactionCase


class TestCrmReferred(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.referred = cls.env["crm.referred"].create(
            [{"name": "Referred 1"}, {"name": "Referred 2"}]
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.referred_1, cls.referred_2 = cls.referred[0], cls.referred[1]
        cls.leads = cls.env["crm.lead"].create(
            [
                {
                    "name": "Test lead 1",
                    "type": "lead",
                    "referred_id": cls.referred_1.id,
                },
                {
                    "name": "Test lead 2",
                    "type": "lead",
                    "referred_id": cls.referred_2.id,
                },
            ]
        )
        cls.lead_1, cls.lead_2 = cls.leads[0], cls.leads[1]

    def test_crm_referred_lead2opportunity_new_customer(self):
        """Check referred is copied to partner when converting lead to
        opportunity creating new customer"""
        convert = (
            self.env["crm.lead2opportunity.partner"]
            .with_context(
                **{
                    "active_model": "crm.lead",
                    "active_id": self.lead_1.id,
                    "active_ids": self.lead_1.ids,
                }
            )
            .create({"name": "convert", "action": "create"})
        )
        convert.action_apply()
        self.assertEqual(self.lead_1.partner_id.referred_id, self.referred_1)
