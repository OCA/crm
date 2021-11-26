# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common


class TestCrmSalespersonPlannerVisit(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            "active_model": self.visit_model,
            "active_ids": self.visit1.ids,
            "active_id": self.visit1.id,
            "att_close_type": att_close_type,
        }
        close_wiz = self.close_wiz_model.with_context(**additionnal_context).create(
            vals
        )
        close_wiz.action_close_reason_apply()

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
