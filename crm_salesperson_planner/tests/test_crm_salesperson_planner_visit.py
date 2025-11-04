# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, fields
from odoo.exceptions import ValidationError
from odoo.tests import common
from odoo.tools import mute_logger


class TestCrmSalespersonPlannerVisitBase(common.TransactionCase):
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
        cls.visit_model = cls.env["crm.salesperson.planner.visit"]
        cls.partner_model = cls.env["res.partner"]
        cls.close_model = cls.env["crm.salesperson.planner.visit.close.reason"]
        cls.close_wiz_model = cls.env["crm.salesperson.planner.visit.close.wiz"]
        cls.partner1 = cls.partner_model.create(
            {
                "name": "Partner Visit 1",
                "email": "partner.visit.1@example.com",
                "phone": "1234567890",
            }
        )
        cls.partner1_contact1 = cls.partner_model.create(
            {
                "name": "Partner Contact Visit 1",
                "email": "partner.visit.1@example.com",
                "phone": "1234567890",
                "parent_id": cls.partner1.id,
            }
        )
        cls.visit1 = cls.visit_model.create({"partner_id": cls.partner1.id})
        cls.visit2 = cls.visit_model.create(
            {"partner_id": cls.partner1_contact1.id, "sequence": 1}
        )
        cls.cancel = cls.close_model.create(
            {
                "name": "Cancel",
                "close_type": "cancel",
                "require_image": False,
                "reschedule": False,
            }
        )
        cls.cancel_resch = cls.close_model.create(
            {
                "name": "Cancel",
                "close_type": "cancel",
                "require_image": False,
                "reschedule": True,
            }
        )
        cls.cancel_img = cls.close_model.create(
            {
                "name": "Cancel",
                "close_type": "cancel",
                "require_image": True,
                "reschedule": False,
            }
        )
        cls.incident = cls.close_model.create(
            {
                "name": "Incident",
                "close_type": "incident",
                "require_image": False,
                "reschedule": False,
            }
        )


class TestCrmSalespersonPlannerVisit(TestCrmSalespersonPlannerVisitBase):
    def test_crm_salesperson_planner_visit(self):
        self.assertNotEqual(self.visit1.name, "/")
        self.assertEqual(self.visit1.state, "draft")
        self.assertEqual(self.partner1.salesperson_planner_visit_count, 2)
        self.assertEqual(self.partner1_contact1.salesperson_planner_visit_count, 1)
        self.assertEqual(self.visit1.date, fields.Date.context_today(self.visit1))
        self.assertEqual(
            self.visit_model.search(
                [("partner_id", "child_of", self.partner1.id)], limit=1
            ),
            self.visit2,
        )

    def config_close_wiz(self, att_close_type, vals):
        additionnal_context = {
            "active_model": self.visit_model._name,
            "active_ids": self.visit1.ids,
            "active_id": self.visit1.id,
            "att_close_type": att_close_type,
        }
        close_wiz = self.close_wiz_model.with_context(**additionnal_context).create(
            vals
        )
        close_wiz.action_close_reason_apply()

    @mute_logger("odoo.models.unlink")
    def test_crm_salesperson_close_wiz_cancel(self):
        self.visit1.action_confirm()
        self.assertEqual(self.visit1.state, "confirm")
        self.config_close_wiz("close", {"reason_id": self.cancel.id, "notes": "Test"})
        self.assertEqual(self.visit1.state, "cancel")
        self.assertEqual(self.visit1.close_reason_id.id, self.cancel.id)
        self.assertEqual(self.visit1.close_reason_notes, "Test")
        self.assertEqual(
            self.visit_model.search_count(
                [("partner_id", "child_of", self.partner1.id)]
            ),
            2,
        )

    @mute_logger("odoo.models.unlink")
    def test_crm_salesperson_close_wiz_cancel_resch(self):
        self.visit1.action_confirm()
        self.assertEqual(self.visit1.state, "confirm")
        self.config_close_wiz(
            "close",
            {
                "reason_id": self.cancel_resch.id,
                "new_date": self.visit1.date + relativedelta(days=10),
                "new_sequence": 40,
            },
        )
        self.assertEqual(self.visit1.close_reason_id.id, self.cancel_resch.id)
        self.assertEqual(
            self.visit_model.search_count(
                [
                    ("partner_id", "=", self.partner1.id),
                    ("date", "=", self.visit1.date + relativedelta(days=10)),
                    ("sequence", "=", 40),
                    ("state", "=", "confirm"),
                ]
            ),
            1,
        )

    @mute_logger("odoo.models.unlink")
    def test_crm_salesperson_close_wiz_cancel_img(self):
        self.visit1.action_confirm()
        self.assertEqual(self.visit1.state, "confirm")
        detail_image = b"R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
        self.config_close_wiz(
            "close", {"reason_id": self.cancel_img.id, "image": detail_image}
        )
        self.assertEqual(self.visit1.close_reason_id.id, self.cancel_img.id)
        self.assertEqual(self.visit1.close_reason_image, detail_image)

    def test_crm_salesperson_close_wiz_incident(self):
        self.visit1.action_confirm()
        self.assertEqual(self.visit1.state, "confirm")
        self.config_close_wiz("incident", {"reason_id": self.incident.id})
        self.assertEqual(self.visit1.state, "incident")

    def test_write_method_updates_calendar_event_user_id(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        visit = self.env["crm.salesperson.planner.visit"].create(
            {
                "name": "Test Visit",
                "user_id": self.env.ref("base.user_demo").id,
                "partner_id": partner.id,
            }
        )
        calendar_event = self.env["calendar.event"].create(
            {
                "name": "Test Event",
                "user_id": self.env.ref("base.user_demo").id,
                "partner_id": partner.id,
            }
        )
        visit.write({"calendar_event_id": calendar_event.id})

        new_user = self.env.ref("base.user_admin")
        visit.write({"user_id": new_user.id})

        self.assertEqual(calendar_event.user_id, new_user)

    def test_action_done(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Ejemplo de partner",
            }
        )
        visit = self.env["crm.salesperson.planner.visit"].create(
            {
                "state": "confirm",
                "partner_id": partner.id,
            }
        )

        visit.action_done()

        self.assertEqual(visit.state, "done")

        with self.assertRaises(ValidationError):
            visit.action_done()

        visit.state = "draft"
        with self.assertRaises(ValidationError):
            visit.action_done()


class TestResPartner(common.TransactionCase):
    def test_action_view_salesperson_planner_visit(self):
        partner = self.env["res.partner"].create(
            {"name": "Test Partner", "is_company": True}
        )

        action = partner.action_view_salesperson_planner_visit()

        self.assertEqual(action["domain"], [("partner_id", "child_of", partner.id)])
        self.assertEqual(action["res_model"], "crm.salesperson.planner.visit")
        self.assertIn("tree", action["view_mode"])
        self.assertIn("form", action["view_mode"])
        self.assertIn("pivot", action["view_mode"])


class TestCalendarEvent(common.TransactionCase):
    def test_write_user_id(self):
        event = self.env["calendar.event"].create({"name": "Test Event"})

        values = {"user_id": 1}

        event.write(values)

        self.assertIn("user_id", values)
        self.assertEqual(values["user_id"], 1)


class TestCrmSalespersonPlannerVisitTemplate(common.TransactionCase):
    def test_partner_ids_constraint(self):
        template = self.env["crm.salesperson.planner.visit.template"].create(
            {
                "name": "Test Visit Template",
                "partner_ids": [(0, 0, {"name": "Customer 1"})],
            }
        )

        with self.assertRaises(ValidationError) as context:
            template.partner_ids = [
                (0, 0, {"name": "Customer 2"}),
                (0, 0, {"name": "Customer 3"}),
            ]

        error_msg = _("Only one customer is allowed")
        self.assertEqual(str(context.exception), error_msg)

    def test_action_view_salesperson_planner_visit(self):
        template = self.env["crm.salesperson.planner.visit.template"].create(
            {
                "partner_id": 1,
                "description": "Ejemplo de descripción",
            }
        )

        action = template.action_view_salesperson_planner_visit()

        self.assertIsInstance(action, dict)
        self.assertEqual(action.get("type"), "ir.actions.act_window")

        expected_domain = [("id", "=", template.visit_ids.ids)]
        self.assertEqual(action.get("domain"), expected_domain)

        expected_context = {
            "default_partner_id": template.partner_id.id,
            "default_visit_template_id": template.id,
            "default_description": template.description,
        }
        self.assertEqual(action.get("context"), expected_context)

    def test_action_cancel(self):
        template = self.env["crm.salesperson.planner.visit.template"].create(
            {
                "state": "in-progress",
            }
        )

        template.action_cancel()

        self.assertEqual(template.state, "cancel")

    def test_action_draft(self):
        template = self.env["crm.salesperson.planner.visit.template"].create(
            {
                "state": "cancel",
            }
        )

        template.action_draft()

        self.assertEqual(template.state, "draft")


class TestCrmSalespersonPlannerVisitTemplateCreate(common.TransactionCase):
    def test_default_date_to(self):
        wizard = self.env["crm.salesperson.planner.visit.template.create"].create({})

        template = self.env["crm.salesperson.planner.visit.template"].create(
            {
                "last_visit_date": fields.Date.today(),
            }
        )
        wizard = wizard.with_context(active_id=template.id)

        default_date_to = wizard._default_date_to()

        expected_date = template.last_visit_date + timedelta(days=7)
        self.assertEqual(default_date_to, expected_date)
