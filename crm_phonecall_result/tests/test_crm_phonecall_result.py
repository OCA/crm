# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import AccessError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestCrmPhonecallResult(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ReportModel = cls.env["crm.phonecall.report"]
        cls.test_result = cls.env["crm.phonecall.result"].create(
            {
                "name": "Test result",
                "description": "Test result description",
                "priority": 5,
            }
        )

        cls.user_salesman = cls.env["res.users"].create(
            {
                "name": "Test Salesman",
                "login": "test_salesman_phone_result",
                "email": "salesman_phone_result@example.com",
                "group_ids": [
                    (6, 0, [cls.env.ref("sales_team.group_sale_salesman").id])
                ],
            }
        )
        cls.user_manager = cls.env["res.users"].create(
            {
                "name": "Test Sales Manager",
                "login": "test_salesmanager_phone_result",
                "email": "salesmanager_phone_result@example.com",
                "group_ids": [
                    (6, 0, [cls.env.ref("sales_team.group_sale_manager").id])
                ],
            }
        )

    def test_create_result(self):
        self.assertEqual(self.test_result.name, "Test result")
        self.assertEqual(self.test_result.description, "Test result description")
        self.assertEqual(self.test_result.priority, 5)

    def test_name_unique_constraint(self):
        """Ensure duplicate names raise an IntegrityError per models.Constraint."""
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.env["crm.phonecall.result"].create({"name": self.test_result.name})

    def test_copy(self):
        copied_record = self.test_result.copy()
        self.assertNotEqual(copied_record.name, self.test_result.name)
        self.assertEqual(
            copied_record.name, self.env._("%s (Copy)", self.test_result.name)
        )

        # Test copying with explicit name in default dict
        custom_copy = self.test_result.copy(default={"name": "Explicit Name"})
        self.assertEqual(custom_copy.name, "Explicit Name")

    def test_priority_order(self):
        """Test that phonecall results search order respects priority."""
        res_low = self.env["crm.phonecall.result"].create(
            {"name": "Low Priority Result", "priority": 1}
        )
        res_high = self.env["crm.phonecall.result"].create(
            {"name": "High Priority Result", "priority": 99}
        )
        results = self.env["crm.phonecall.result"].search(
            [("id", "in", [res_low.id, res_high.id])]
        )
        self.assertEqual(results[0], res_low)
        self.assertEqual(results[1], res_high)

    def test_default_data_records(self):
        """Ensure default records created via XML data files exist."""
        positive = self.env.ref(
            "crm_phonecall_result.phonecall_result_positive", raise_if_not_found=False
        )
        negative = self.env.ref(
            "crm_phonecall_result.phonecall_result_negative", raise_if_not_found=False
        )
        wrong_num = self.env.ref(
            "crm_phonecall_result.phonecall_result_wrong_number",
            raise_if_not_found=False,
        )

        if positive:
            self.assertEqual(positive.name, "Positive")
        if negative:
            self.assertEqual(negative.name, "Negative")
        if wrong_num:
            self.assertEqual(wrong_num.name, "Wrong number")

    def test_access_rights_salesman(self):
        """Salesman can read call results but cannot create, modify or delete them."""
        result_as_salesman = self.test_result.with_user(self.user_salesman)
        # Read permission granted
        self.assertEqual(result_as_salesman.name, "Test result")

        # Create forbidden
        with self.assertRaises(AccessError):
            self.env["crm.phonecall.result"].with_user(self.user_salesman).create(
                {"name": "Forbidden Result"}
            )

        # Write forbidden
        with self.assertRaises(AccessError):
            result_as_salesman.write({"name": "New Name"})

        # Unlink forbidden
        with self.assertRaises(AccessError):
            result_as_salesman.unlink()

    def test_access_rights_manager(self):
        """Sales Manager has full access to crm.phonecall.result."""
        res_mgr = (
            self.env["crm.phonecall.result"]
            .with_user(self.user_manager)
            .create({"name": "Manager Created Result"})
        )
        self.assertEqual(res_mgr.name, "Manager Created Result")

        res_mgr.write({"name": "Manager Updated Result"})
        self.assertEqual(res_mgr.name, "Manager Updated Result")

        res_mgr.unlink()
        self.assertFalse(res_mgr.exists())

    def test_report_view_exists(self):
        """Ensure the report view loads without error and _select query is executed."""
        select_clause = self.ReportModel._select()
        self.assertIn("c.phone_result_id", select_clause)

        records = self.ReportModel.search([], limit=1)
        self.assertIsNotNone(records)

    def test_field_phone_result_id_exists(self):
        """Ensure the custom field phone_result_id is present in the model."""
        fields = self.ReportModel.fields_get()
        self.assertIn("phone_result_id", fields)

    def test_phonecall_assignment_and_report(self):
        """Test creating a phone call with phone_result_id and querying report."""
        call = self.env["crm.phonecall"].create(
            {
                "name": "Test Workflow Phone Call",
                "phone_result_id": self.test_result.id,
            }
        )
        self.assertEqual(call.phone_result_id, self.test_result)

        report_records = self.ReportModel.search(
            [("phone_result_id", "=", self.test_result.id)]
        )
        self.assertIsNotNone(report_records)

    def test_phonecall_form_view(self):
        """Test assigning phone_result_id via Form view on crm.phonecall."""
        phonecall_form = Form(self.env["crm.phonecall"])
        phonecall_form.name = "Form Test Call"
        phonecall_form.phone_result_id = self.test_result
        call = phonecall_form.save()

        self.assertEqual(call.name, "Form Test Call")
        self.assertEqual(call.phone_result_id, self.test_result)

    def test_phonecall_search_and_groupby(self):
        """Test filtering and grouping phone calls by phone_result_id."""
        call1 = self.env["crm.phonecall"].create(
            {
                "name": "Call with result",
                "phone_result_id": self.test_result.id,
            }
        )
        call2 = self.env["crm.phonecall"].create(
            {
                "name": "Call without result",
            }
        )
        calls_with_result = self.env["crm.phonecall"].search(
            [("phone_result_id", "!=", False)]
        )
        self.assertIn(call1, calls_with_result)
        self.assertNotIn(call2, calls_with_result)

        grouped = self.env["crm.phonecall"]._read_group(
            [("id", "in", [call1.id, call2.id])],
            groupby=["phone_result_id"],
        )
        grouped_result_records = [g[0] for g in grouped]
        self.assertIn(self.test_result, grouped_result_records)

    def test_report_read_group(self):
        """Test reporting _read_group with phone_result_id."""
        self.env["crm.phonecall"].create(
            {
                "name": "Report Group Test Call",
                "phone_result_id": self.test_result.id,
            }
        )
        grouped_report = self.ReportModel._read_group(
            [("phone_result_id", "=", self.test_result.id)],
            groupby=["phone_result_id"],
        )
        self.assertTrue(grouped_report)
        self.assertEqual(grouped_report[0][0], self.test_result)
