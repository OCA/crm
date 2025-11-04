# Copyright 2021 Sygel - Valentin Vinagre
# Copyright 2021 Sygel - Manuel Regidor
# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from datetime import timedelta

from freezegun import freeze_time

from odoo import exceptions, fields
from odoo.tests import common
from odoo.tools import mute_logger


class TestCrmSalespersonPlannerVisitTemplate(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
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
        self.assertEqual(len(self.visit_template_base.visit_ids), 4)
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
        self.visit_template_base.create_visits(days=10)
        self.assertEqual(len(self.visit_template_base.visit_ids), 10)
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
        self.assertEqual(len(self.visit_template_base.visit_ids), 4)
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
        self.visit_template_base.create_visits(days=10)
        self.assertEqual(len(self.visit_template_base.visit_ids), 10)
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

    @mute_logger("odoo.models.unlink")
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

    def test_05_repeat_weeks(self):
        self.visit_template_base.write(
            {
                "start_date": fields.Date.today(),
                "interval": 1,
                "rrule_type": "weekly",
                "tue": True,
                "end_type": "end_date",
                "until": fields.Date.today() + timedelta(days=90),
            }
        )

        dates = [
            self.visit_template_base.start_date + timedelta(days=i) for i in range(91)
        ]
        filtered_tue_dates = [d for d in dates if d.weekday() == 1]

        self.visit_template_base.action_validate()
        self.assertFalse(self.visit_template_base.visit_ids)
        create_model = self.env["crm.salesperson.planner.visit.template.create"]
        create_item = create_model.with_context(
            active_id=self.visit_template_base.id
        ).create({"date_to": filtered_tue_dates[2]})
        create_item.create_visits()
        self.assertEqual(self.visit_template_base.state, "done")
        visit_dates = self.visit_template_base.visit_ids.mapped("date")
        self.assertIn(fields.Date.from_string(filtered_tue_dates[4]), visit_dates)
        self.assertEqual(
            self.visit_template_base.last_visit_date,
            fields.Date.from_string(filtered_tue_dates[len(filtered_tue_dates) - 1]),
        )

    @freeze_time("2024-11-01")
    def test_06_repeat_months_count_01(self):
        self.visit_template_base.write(
            {
                "start_date": "2024-03-08",
                "interval": 1,
                "rrule_type": "monthly",
                "end_type": "count",
                "count": 2,
                "month_by": "date",
                "day": 1,
            }
        )
        self.visit_template_base.action_validate()
        self.assertFalse(self.visit_template_base.visit_ids)
        create_model = self.env["crm.salesperson.planner.visit.template.create"]
        create_item = create_model.with_context(
            active_id=self.visit_template_base.id
        ).create({"date_to": "2024-12-13"})
        create_item.create_visits()
        self.assertEqual(self.visit_template_base.state, "done")
        self.assertEqual(len(self.visit_template_base.visit_ids), 2)
        visit_dates = self.visit_template_base.visit_ids.mapped("date")
        self.assertIn(fields.Date.from_string("2024-04-01"), visit_dates)
        self.assertEqual(
            self.visit_template_base.last_visit_date,
            fields.Date.from_string("2024-05-01"),
        )

    @freeze_time("2024-11-01")
    def test_06_repeat_months_count_02(self):
        self.visit_template_base.write(
            {
                "start_date": "2024-03-08",
                "interval": 1,
                "rrule_type": "monthly",
                "end_type": "count",
                "count": 2,
                "month_by": "date",
                "day": 1,
            }
        )
        self.visit_template_base.action_validate()
        self.assertFalse(self.visit_template_base.visit_ids)
        create_model = self.env["crm.salesperson.planner.visit.template.create"]
        create_item = create_model.with_context(
            active_id=self.visit_template_base.id
        ).create({"date_to": "2024-12-13"})
        create_item.create_visits()
        self.assertEqual(self.visit_template_base.state, "done")
        self.assertEqual(len(self.visit_template_base.visit_ids), 2)
        visit_dates = self.visit_template_base.visit_ids.mapped("date")
        self.assertIn(fields.Date.from_string("2024-04-01"), visit_dates)
        self.assertEqual(
            self.visit_template_base.last_visit_date,
            fields.Date.from_string("2024-05-01"),
        )

    @freeze_time("2024-11-01")
    def test_06_repeat_months_count_03(self):
        self.visit_template_base.write(
            {
                "start_date": "2024-03-08",
                "interval": 1,
                "rrule_type": "monthly",
                "end_type": "count",
                "count": 2,
                "month_by": "day",
                "byday": "1",
                "weekday": "MON",
            }
        )
        self.visit_template_base.action_validate()
        self.assertFalse(self.visit_template_base.visit_ids)
        create_model = self.env["crm.salesperson.planner.visit.template.create"]
        create_item = create_model.with_context(
            active_id=self.visit_template_base.id
        ).create({"date_to": "2024-12-13"})
        create_item.create_visits()
        self.assertEqual(self.visit_template_base.state, "done")
        self.assertEqual(len(self.visit_template_base.visit_ids), 2)
        visit_dates = self.visit_template_base.visit_ids.mapped("date")
        self.assertIn(fields.Date.from_string("2024-04-01"), visit_dates)
        self.assertEqual(
            self.visit_template_base.last_visit_date,
            fields.Date.from_string("2024-05-06"),
        )

    def test_07_repeat_yearly_count_01(self):
        self.visit_template_base.write(
            {
                "start_date": "2024-03-08",
                "interval": 1,
                "rrule_type": "yearly",
                "end_type": "count",
                "count": 2,
            }
        )
        self.visit_template_base.action_validate()
        self.assertFalse(self.visit_template_base.visit_ids)
        create_model = self.env["crm.salesperson.planner.visit.template.create"]
        create_item = create_model.with_context(
            active_id=self.visit_template_base.id
        ).create({"date_to": "2030-01-01"})
        create_item.create_visits()
        self.assertEqual(self.visit_template_base.state, "done")
        self.assertEqual(len(self.visit_template_base.visit_ids), 2)
        visit_dates = self.visit_template_base.visit_ids.mapped("date")
        self.assertIn(fields.Date.from_string("2024-03-08"), visit_dates)
        self.assertEqual(
            self.visit_template_base.last_visit_date,
            fields.Date.from_string("2025-03-08"),
        )
