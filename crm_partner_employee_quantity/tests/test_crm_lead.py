# Copyright 2026 Binhex - Adasat Torres de León
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo.addons.base.tests.common import BaseCommon


class TestCrmLead(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.employee_quantity_range = (
            cls.env["res.partner.employee_quantity_range"]
            .create({"name": "0-10 people"})
            .id
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "New test lead",
                "type": "lead",
                "partner_name": "Test company",
                "employee_quantity": 7,
                "employee_quantity_range_id": cls.employee_quantity_range,
            }
        )

    def test_create_a_partner_from_lead(self):
        self.lead._handle_partner_assignment(
            force_partner_id=False,
            create_missing=True,
        )
        partner_id = self.lead.partner_id
        self.assertEqual(partner_id.employee_quantity, 7)
        self.assertEqual(
            partner_id.employee_quantity_range_id.id,
            self.employee_quantity_range,
        )
