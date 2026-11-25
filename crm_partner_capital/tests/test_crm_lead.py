# Copyright 2026 Binhex - Adasat Torres de León
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo.addons.base.tests.common import BaseCommon


class TestCrmLead(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.country_id = (
            cls.env["res.country"].create({"name": "Test country", "code": "AA"}).id
        )
        cls.currency_id = cls.env.ref("base.EUR").id
        cls.turnover_range_id = (
            cls.env["res.partner.turnover_range"].create({"name": "1-100"}).id
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "New test lead",
                "capital_country_id": cls.country_id,
                "capital_currency_id": cls.currency_id,
                "turnover_amount": 100.0,
                "turnover_range_id": cls.turnover_range_id,
                "company_size": "micro",
                "type": "lead",
                "partner_name": "Test company",
            }
        )

    def test_create_a_partner_from_lead(self):
        self.lead._handle_partner_assignment(
            force_partner_id=False,
            create_missing=True,
        )
        partner_id = self.lead.partner_id
        self.assertEqual(partner_id.capital_country_id.id, self.country_id)
        self.assertEqual(partner_id.capital_currency_id.id, self.currency_id)
        self.assertEqual(partner_id.turnover_amount, 100.0)
        self.assertEqual(partner_id.turnover_range_id.id, self.turnover_range_id)
        self.assertEqual(partner_id.company_size, "micro")
