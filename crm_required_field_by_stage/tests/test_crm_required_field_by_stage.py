# Copyright 2024 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import ast

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestCrmRequiredFieldByStage(TransactionCase):
    def setUp(self):
        super().setUp()

        self.crm_stage_model = self.env["crm.stage"]
        self.crm_lead_model = self.env["crm.lead"]
        self.crm_stage_1 = self.crm_stage_model.create(
            {
                "name": "CRM Stage 1",
                "required_field_ids": [
                    (4, self.env.ref("crm.field_crm_lead__phone").id)
                ],
            }
        )
        self.crm_lead_1 = self.crm_lead_model.create(
            {
                "name": "CRM Lead 1",
            }
        )

    def test_locking(self):
        with self.assertRaises(UserError):
            self.crm_lead_1.write(
                {
                    "stage_id": self.crm_stage_1.id,
                }
            )
        self.assertTrue(self.crm_lead_1.stage_id)
        self.crm_lead_1.write(
            {
                "phone": "(00) 0000-0000",
            }
        )
        self.crm_lead_1.write(
            {
                "stage_id": self.crm_stage_1.id,
            }
        )
        self.assertEqual(self.crm_lead_1.stage_id.id, self.crm_stage_1.id)

    def test_get_view_required_fields(self):
        arch, view = self.crm_lead_1._get_view(view_type="form")
        node = arch.xpath("//field[@name='phone']")
        self.assertTrue(node)
        attrs = ast.literal_eval(node[0].attrib.get("attrs", "{}"))
        self.assertIn("required", attrs)
        self.assertIn(self.crm_stage_1.id, attrs["required"][0][2])
