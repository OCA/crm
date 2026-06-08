from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import RecordCapturer, TransactionCase, new_test_user


class TestCrmRecurringActivity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test.partner@example.com",
            }
        )

        cls.company = cls.env["res.company"].create(
            {
                "name": "Test Company Name",
                "partner_id": cls.partner.id,
            }
        )

        cls.user = new_test_user(
            cls.env,
            login="test_user",
            groups="base.group_user",
            company_id=cls.company.id,
            company_ids=[Command.set([cls.company.id])],
        )

        cls.team = cls.env["crm.team"].create(
            {
                "name": "Test Sales Team",
                "company_id": cls.company.id,
            }
        )

        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Opportunity",
                "partner_id": cls.partner.id,
                "team_id": cls.team.id,
                "type": "opportunity",
                "company_id": cls.company.id,
            }
        )

        cls.activity_type = cls.env["mail.activity.type"].create(
            {
                "name": "Test Activity Type",
                "summary": "Default summary",
                "default_note": "<p>Default note</p>",
                "res_model": "crm.lead",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "service",
            }
        )

    def _create_recurring_activity(self, **kwargs):
        vals = {
            "company_id": self.company.id,
            "activity_type_id": self.activity_type.id,
            "user_id": self.user.id,
            "scheduled_days": 3,
        }
        vals.update(kwargs)
        return self.env["crm.recurring.activity"].create(vals)

    def test_create_recurring_activity(self):
        """The recurring activity is created using the specified values,
        and the fields take their default values from the activity type.
        """
        recurring = self._create_recurring_activity()

        self.assertTrue(recurring, "Recurring activity wasn't created.")
        # Compute fields
        self.assertEqual(recurring.summary, self.activity_type.summary)
        self.assertEqual(recurring.note, self.activity_type.default_note)

    def test_explicit_summary_is_preserved(self):
        """If the summary and note are explicitly specified,
        the compute does not overwrite them.
        """
        recurring = self._create_recurring_activity(
            summary="Custom summary",
            note="<p>Custom note</p>",
        )

        self.assertEqual(recurring.summary, "Custom summary")
        self.assertIn("Custom note", recurring.note)

    def test_constraint_user_without_company_access(self):
        """You cannot assign a recurring activity to a user
        who does not have access to the specified company.
        """
        other_company = self.env["res.company"].create({"name": "Other Company"})
        with self.assertRaises(ValidationError):
            self._create_recurring_activity(company_id=other_company.id)

    def test_sale_order_confirm_schedules_multiple_activities(self):
        """All of the company’s recurring activities are scheduled."""
        self._create_recurring_activity(scheduled_days=1, summary="Mail")
        self._create_recurring_activity(scheduled_days=7, summary="Call")
        self._create_recurring_activity(scheduled_days=14, summary="Meeting")

        action = self.lead.action_sale_quotations_new()
        order = (
            self.env["sale.order"]
            .with_context(**action["context"])
            .create(
                {
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product.id,
                                "product_uom_qty": 1,
                            }
                        ),
                    ],
                }
            )
        )

        with RecordCapturer(self.env["mail.activity"], []) as rc:
            order.action_confirm()
        new_activities = rc.records

        self.assertEqual(len(new_activities), 3)
        self.assertEqual(
            set(new_activities.mapped("summary")),
            {"Mail", "Call", "Meeting"},
        )

    def test_sale_order_confirm_without_opportunity(self):
        """If the sale.order does not have an opportunity_id,
        no task is scheduled and action_confirm works as normal.
        """
        self._create_recurring_activity()

        action = self.lead.action_sale_quotations_new()
        order = (
            self.env["sale.order"]
            .with_context(**action["context"])
            .create(
                {
                    "opportunity_id": None,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product.id,
                                "product_uom_qty": 1,
                            }
                        ),
                    ],
                }
            )
        )

        activities_before = self.lead.activity_ids
        order.action_confirm()

        self.assertEqual(order.state, "sale")
        self.assertEqual(self.lead.activity_ids, activities_before)
