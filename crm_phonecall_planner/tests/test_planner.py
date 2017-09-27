# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from __future__ import division
from datetime import timedelta
from openerp import fields
from openerp.exceptions import ValidationError
from openerp.tests.common import SavepointCase
from openerp.tools import float_compare


class PlannerCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(PlannerCase, cls).setUpClass()
        cls.mondays = cls.env["resource.calendar"].create({
            "name": "mondays",
            "attendance_ids": [
                (0, 0, {
                    "name": "Monday morning",
                    "dayofweek": "0",
                    "hour_from": 9,
                    "hour_to": 12,
                }),
                (0, 0, {
                    "name": "Monday evening",
                    "dayofweek": "0",
                    "hour_from": 15,
                    "hour_to": 20,
                }),
            ]
        })
        cls.tuesdays = cls.env["resource.calendar"].create({
            "name": "tuesdays",
            "attendance_ids": [
                (0, 0, {
                    "name": "Tuesday morning",
                    "dayofweek": "1",
                    "hour_from": 9,
                    "hour_to": 12,
                }),
                (0, 0, {
                    "name": "One Tuesday evening",
                    "dayofweek": "1",
                    "hour_from": 15,
                    "hour_to": 20,
                    "date_from": "2017-10-02",
                    "date_to": "2017-10-08",
                }),
            ]
        })
        cls.partners = cls.env["res.partner"].create({
            "name": "partner0",
        })
        cls.partners += cls.env["res.partner"].create({
            "name": "partner1",
            "phonecall_calendar_ids": [(6, 0, cls.mondays.ids)],
        })
        cls.partners += cls.env["res.partner"].create({
            "name": "partner2",
            "phonecall_calendar_ids": [(6, 0, cls.tuesdays.ids)],
        })
        cls.partners += cls.env["res.partner"].create({
            "name": "partner3",
            "phonecall_calendar_ids": [
                (6, 0, (cls.mondays | cls.tuesdays).ids),
            ],
        })
        cls.wizard = cls.env["crm.phonecall.planner"].with_context(tz="UTC") \
            .create({
                "name": "Test call",
                "start": "2017-09-20 08:00:00",
                "end": "2017-10-20 16:00:00",
                "duration": 1,
                "res_partner_domain": str([("id", "in", cls.partners.ids)]),
            })

    def test_defaults(self):
        """The planner provides the expected default values."""
        wizard = self.wizard.create({
            "name": "Test defaults!",
        })
        self.assertEqual(0, float_compare(wizard.duration, 7 / 60, 6))
        self.assertLessEqual(wizard.start, fields.Datetime.now())
        start = fields.Datetime.from_string(wizard.start)
        end = fields.Datetime.from_string(wizard.end)
        self.assertEqual(end, start + timedelta(days=30, hours=8))

    def test_start_before_end(self):
        """A wizard with start date bigger than end date is not allowed."""
        with self.assertRaises(ValidationError):
            self.wizard.write({
                "start": self.wizard.end,
                "end": self.wizard.start,
            })

    def test_plan_no_repeat(self):
        """The planner creates one call per partner."""
        self.wizard.action_accept()
        expected_dates = {
            "2017-09-25 09:00:00",
            "2017-09-25 10:00:00",
            "2017-09-26 09:00:00",
        }
        real_dates = self.wizard.planned_calls.mapped("date")
        self.assertEqual(expected_dates, set(real_dates))
        self.assertEqual(len(expected_dates), len(real_dates))
        self.assertEqual(
            self.wizard.planned_calls.mapped("partner_id"),
            self.partners[1:]
        )

    def test_plan_repeat(self):
        """The planner repeats calls each day."""
        self.wizard.write({
            "repeat_calls": True,
            "start": "2017-09-20 12:00:00",
        })
        self.wizard.action_accept()
        expected_dates = {
            '2017-09-25 12:00:00',
            '2017-09-25 15:00:00',
            '2017-09-26 12:00:00',
            '2017-10-02 12:00:00',
            '2017-10-02 15:00:00',
            '2017-10-03 12:00:00',
            '2017-10-03 15:00:00',
            '2017-10-09 12:00:00',
            '2017-10-09 15:00:00',
            '2017-10-10 12:00:00',
            '2017-10-16 12:00:00',
            '2017-10-16 15:00:00',
            '2017-10-17 12:00:00',
        }
        real_dates = self.wizard.planned_calls.mapped("date")
        self.assertEqual(expected_dates, set(real_dates))
        self.assertEqual(len(expected_dates), len(real_dates))
        self.assertEqual(
            self.wizard.planned_calls.mapped("partner_id"),
            self.partners[1:]
        )
