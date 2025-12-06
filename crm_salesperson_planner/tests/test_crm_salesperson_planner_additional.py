# Copyright 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import common
from odoo.tools import mute_logger


class TestCalendarEventAdditional(common.TransactionCase):
    def test_write_updates_partner_ids_on_user_change(self):
        partner = self.env["res.partner"].create({"name": "Partner"})
        user_demo = self.env.ref("base.user_demo")
        user_admin = self.env.ref("base.user_admin")

        visit = self.env["crm.salesperson.planner.visit"].create(
            {
                "name": "Visit Partner Update",
                "user_id": user_demo.id,
                "partner_id": partner.id,
            }
        )

        event = self.env["calendar.event"].create(
            {
                "name": "Event Partner Update",
                "user_id": user_demo.id,
                "res_model": "crm.salesperson.planner.visit",
                "res_id": visit.id,
                "partner_ids": [(6, 0, [partner.id, user_demo.partner_id.id])],
            }
        )

        # Sanity check
        self.assertIn(user_demo.partner_id.id, event.partner_ids.ids)
        self.assertIn(partner.id, event.partner_ids.ids)

        # Update user -> partner_ids should be updated to include admin partner id
        event.write({"user_id": user_admin.id})
        event.refresh()

        self.assertIn(user_admin.partner_id.id, event.partner_ids.ids)
        self.assertNotIn(user_demo.partner_id.id, event.partner_ids.ids)
        self.assertIn(partner.id, event.partner_ids.ids)

    def test_unlink_multiple_events_with_visit_messages(self):
        visitor_user = self.env.ref("base.user_demo")
        partner1 = self.env["res.partner"].create({"name": "Partner 1"})
        partner2 = self.env["res.partner"].create({"name": "Partner 2"})

        visit1 = self.env["crm.salesperson.planner.visit"].create(
            {
                "name": "Visit Unlink 1",
                "user_id": visitor_user.id,
                "partner_id": partner1.id,
            }
        )
        visit2 = self.env["crm.salesperson.planner.visit"].create(
            {
                "name": "Visit Unlink 2",
                "user_id": visitor_user.id,
                "partner_id": partner2.id,
            }
        )

        event1 = self.env["calendar.event"].create(
            {
                "name": "Event Unlink 1",
                "user_id": visitor_user.id,
                "res_model": "crm.salesperson.planner.visit",
                "res_id": visit1.id,
                "partner_ids": [(6, 0, [partner1.id, visitor_user.partner_id.id])],
            }
        )
        event2 = self.env["calendar.event"].create(
            {
                "name": "Event Unlink 2",
                "user_id": visitor_user.id,
                "res_model": "crm.salesperson.planner.visit",
                "res_id": visit2.id,
                "partner_ids": [(6, 0, [partner2.id, visitor_user.partner_id.id])],
            }
        )

        # combined unlink should raise with both messages
        with self.assertRaises(ValidationError) as context:
            (event1 | event2).unlink()

        msg = str(context.exception)
        self.assertIn("Event Event Unlink 1 is related to salesperson visit", msg)
        self.assertIn("Event Event Unlink 2 is related to salesperson visit", msg)


class TestVisitEventUpdates(common.TransactionCase):
    def test_visit_write_updates_calendar_event_start_stop(self):
        partner = self.env["res.partner"].create({"name": "Partner Visit Date"})
        visitor_user = self.env.ref("base.user_demo")

        visit = self.env["crm.salesperson.planner.visit"].create(
            {
                "name": "Visit Date Test",
                "user_id": visitor_user.id,
                "partner_id": partner.id,
            }
        )

        start_dt = fields.Datetime.from_string(fields.Datetime.now())
        event = self.env["calendar.event"].create(
            {
                "name": "Event Visit Date",
                "user_id": visitor_user.id,
                "res_model": "crm.salesperson.planner.visit",
                "res_id": visit.id,
                "start": fields.Datetime.to_string(start_dt),
                "partner_ids": [(6, 0, [partner.id, visitor_user.partner_id.id])],
            }
        )

        # Link event to visit
        visit.write({"calendar_event_id": event.id})

        new_date = (fields.Date.context_today(self) + relativedelta(days=5))
        visit.write({"date": new_date})
        visit.refresh()
        event.refresh()

        # event.start_date should be updated to new date
        self.assertEqual(event.start_date, new_date)

    def test_visit_write_with_bypass_context_does_not_update_event(self):
        partner = self.env["res.partner"].create({"name": "Partner Visit Bypass"})
        visitor_user = self.env.ref("base.user_demo")

        visit = self.env["crm.salesperson.planner.visit"].create(
            {
                "name": "Visit Bypass Test",
                "user_id": visitor_user.id,
                "partner_id": partner.id,
            }
        )

        start_dt = fields.Datetime.from_string(fields.Datetime.now())
        event = self.env["calendar.event"].create(
            {
                "name": "Event Visit Bypass",
                "user_id": visitor_user.id,
                "res_model": "crm.salesperson.planner.visit",
                "res_id": visit.id,
                "start": fields.Datetime.to_string(start_dt),
                "partner_ids": [(6, 0, [partner.id, visitor_user.partner_id.id])],
            }
        )

        # Link event to visit
        visit.write({"calendar_event_id": event.id})

        new_date = (fields.Date.context_today(self) + relativedelta(days=5))
        visit.with_context(bypass_update_event=True).write({"date": new_date})
        visit.refresh()
        event.refresh()

        # event.start_date should NOT be updated
        self.assertNotEqual(event.start_date, new_date)


class TestTemplateWizardAdditional(common.TransactionCase):
    def test_wizard_create_visits_negative_date_raises(self):
        template = self.env["crm.salesperson.planner.visit.template"].create(
            {"last_visit_date": fields.Date.context_today(self) - relativedelta(days=2)}
        )
        wiz = self.env["crm.salesperson.planner.visit.template.create"].create(
            {"date_to": fields.Date.context_today(self) - relativedelta(days=1)}
        )
        wiz = wiz.with_context(active_id=template.id)

        with self.assertRaises(ValidationError):
            wiz.create_visits()
