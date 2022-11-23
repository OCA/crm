# Copyright 2021 Sygel - Valentin Vinagre
# Copyright 2021 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import exceptions, fields
from odoo.tests import common


class TestCrmSalespersonPlannerVisitTemplate(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.visit_template_model = cls.env["crm.salesperson.planner.visit.template"]
        cls.partner_model = cls.env["res.partner"]
        cls.close_reason_mode = cls.env["crm.salesperson.planner.visit.close.reason"]
        cls.partner1 = cls.partner_model.create(
            {
                "name": "Partner Visit 1",
                "email": "partner.visit.1@example.com",
                "phone": "1234567890",
            }
        )
        cls.visit_template_base = cls.visit_template_model.create(
            {
                "partner_ids": [(6, False, cls.partner1.ids)],
                "start_date": fields.Date.today(),
                "stop_date": fields.Date.today(),
                "start": fields.Date.today(),
                "stop": fields.Date.today(),
            }
        )
        cls.close_reason = cls.close_reason_mode.create(
            {"name": "close reason", "close_type": "cancel"}
        )

    def test_01_repeat_days(self):
        self.visit_template_base.write(
            {
                "auto_validate": False,
                "interval": 1,
                "rrule_type": "daily",
                "end_type": "count",
                "count": 10,
            }
        )
        self.visit_template_base.action_validate()
        self.visit_template_base.create_visits(days=4)
        self.assertEqual(self.visit_template_base.visit_ids_count, 4)
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.state == "draft"
                )
            ),
            4,
        )
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.calendar_event_id.id
                )
            ),
            0,
        )
        self.assertEqual(self.visit_template_base.state, "in-progress")
        self.visit_template_base.create_visits(days=9)
        self.visit_template_base._compute_visit_ids_count()
        self.assertEqual(self.visit_template_base.visit_ids_count, 10)
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.state == "draft"
                )
            ),
            10,
        )
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.calendar_event_id.id
                )
            ),
            0,
        )
        self.assertEqual(self.visit_template_base.state, "done")

    def test_02_repeat_days_autovalidate(self):
        self.visit_template_base.write(
            {
                "auto_validate": True,
                "interval": 1,
                "rrule_type": "daily",
                "end_type": "count",
                "count": 10,
            }
        )
        self.visit_template_base.action_validate()
        self.visit_template_base.create_visits(days=4)
        self.assertEqual(self.visit_template_base.visit_ids_count, 4)
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.state == "draft"
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.calendar_event_id.id
                )
            ),
            4,
        )
        self.assertEqual(self.visit_template_base.state, "in-progress")
        self.visit_template_base.create_visits(days=9)
        self.visit_template_base._compute_visit_ids_count()
        self.assertEqual(self.visit_template_base.visit_ids_count, 10)
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.state == "draft"
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                self.visit_template_base.visit_ids.filtered(
                    lambda a: a.calendar_event_id.id
                )
            ),
            10,
        )
        self.assertEqual(self.visit_template_base.state, "done")

    def test_03_change_visit_date(self):
        visit_template = self.visit_template_base.copy()
        visit_template.write(
            {
                "auto_validate": True,
                "interval": 1,
                "rrule_type": "daily",
                "end_type": "count",
                "count": 10,
            }
        )
        visit_template.create_visits(days=10)
        visit_0 = fields.first(visit_template.visit_ids)
        event_id_0 = visit_0.calendar_event_id
        self.assertEqual(visit_0.date, event_id_0.start_date)
        visit_0.write({"date": fields.Date.today() + timedelta(days=7)})
        self.assertEqual(event_id_0.start_date, fields.Date.today() + timedelta(days=7))
        event_id_0.write(
            {
                "start": fields.Datetime.today() + timedelta(days=14),
                "stop": fields.Datetime.today() + timedelta(days=14),
            }
        )
        self.assertEqual(visit_0.date, fields.Date.today() + timedelta(days=14))

    def test_04_cancel_visit(self):
        visit_template = self.visit_template_base.copy()
        visit_template.write(
            {
                "auto_validate": True,
                "interval": 1,
                "rrule_type": "daily",
                "end_type": "count",
                "count": 10,
            }
        )
        visit_template.create_visits(days=10)
        first_visit = fields.first(visit_template.visit_ids)
        self.assertTrue(first_visit.calendar_event_id)
        with self.assertRaises(exceptions.ValidationError):
            first_visit.unlink()
        self.assertEqual(len(visit_template.visit_ids), 10)
        first_visit.action_cancel(self.close_reason)
        self.assertFalse(first_visit.calendar_event_id)
        first_visit.unlink()
        self.assertEqual(len(visit_template.visit_ids), 9)
