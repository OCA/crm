# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.tests.common import TransactionCase


class TestCrmPhonecallResult(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ReportModel = cls.env["crm.phonecall.report"]
        cls.test_result = cls.env["crm.phonecall.result"].create(
            {
                "name": "Test result",
                "priority": 5,
            }
        )

    def test_create_result(self):
        self.assertEqual(self.test_result.name, "Test result")
        self.assertEqual(self.test_result.priority, 5)

    def test_copy(self):
        copied_record = self.test_result.copy()
        self.assertNotEqual(copied_record.name, self.test_result.name)
        self.assertEqual(copied_record.name, _("%s (Copy)") % self.test_result.name)

    def test_report_view_exists(self):
        """Ensure the report view loads without error."""
        records = self.ReportModel.search([], limit=1)
        self.assertIsNotNone(records)

    def test_field_phone_result_id_exists(self):
        """Ensure the custom field phone_result_id is present in the model."""
        fields = self.ReportModel.fields_get()
        self.assertIn("phone_result_id", fields)
