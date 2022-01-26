# Copyright 2022 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestCrmSalespersonPlannerReAssign(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.visit_model = cls.env["crm.salesperson.planner.visit"]
        cls.template_model = cls.env["crm.salesperson.planner.visit.template"]
        cls.partner_model = cls.env["res.partner"]
        cls.users_mode = cls.env["res.users"]
        cls.close_model = cls.env["crm.salesperson.planner.visit.close.reason"]
        cls.close_wiz_model = cls.env["crm.salesperson.planner.visit.close.wiz"]
        cls.reassign_model = cls.env["crm.salesperson.planner.visit.reassign"]
        cls.client = cls.partner_model.create({"name": "Client 1"})
        cls.salesperson1_contact = cls.partner_model.create(
            {"name": "Salesperson 1", "email": "salesperson.1@example.com"}
        )
        cls.salesperson1 = cls.users_mode.create(
            {"name": "Salesperson 1", "login": "salesperson.1@example.com"}
        )
        cls.salesperson2_contact = cls.partner_model.create(
            {"name": "Salesperson 2", "email": "salesperson.2@example.com"}
        )
        cls.salesperson2 = cls.users_mode.create(
            {"name": "Salesperson 2", "login": "salesperson.2@example.com"}
        )
        cls.visit1 = cls.visit_model.create(
            {
                "partner_id": cls.client.id,
                "user_id": cls.salesperson1.id,
                "date": "2022-01-01",
            }
        )
        cls.visit2 = cls.visit_model.create(
            {
                "partner_id": cls.client.id,
                "user_id": cls.salesperson1.id,
                "date": "2022-02-01",
            }
        )
        cls.template = cls.template_model.create(
            {
                "user_id": cls.salesperson1.id,
                "start": "2022-01-01",
                "stop": "2022-02-28",
            }
        )
        cls.reassign = cls.reassign_model.create(
            {
                "search_templates": True,
                "current_user_id": cls.salesperson1.id,
                "new_user_id": cls.salesperson2.id,
            }
        )

    def test_crm_salesperson_reassign_search_visits(self):
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 2)
        self.assertTrue(
            self.visit1.id
            in self.reassign.visit_reassign_line_ids.mapped(
                "crm_salesperson_planner_visit_id"
            ).ids
        )
        self.assertTrue(
            self.visit2.id
            in self.reassign.visit_reassign_line_ids.mapped(
                "crm_salesperson_planner_visit_id"
            ).ids
        )
        self.reassign.write({"start_date": "2022-01-02", "end_date": "2022-02-28"})
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 1)
        self.assertFalse(
            self.visit1.id
            in self.reassign.visit_reassign_line_ids.mapped(
                "crm_salesperson_planner_visit_id"
            ).ids
        )
        self.assertTrue(
            self.visit2.id
            in self.reassign.visit_reassign_line_ids.mapped(
                "crm_salesperson_planner_visit_id"
            ).ids
        )
        self.reassign.write({"search_visits": False})
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 0)
        self.reassign.write(
            {
                "search_visits": True,
                "visit_draft_state": False,
                "visit_cancel_state": True,
            }
        )
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 0)

    def test_crm_salesperson_reassign_search_templates(self):
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.salesperson_reassign_line_ids), 1)
        self.reassign.write({"search_templates": False})
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.salesperson_reassign_line_ids), 0)
        self.reassign.write(
            {
                "search_templates": True,
                "template_draft_state": False,
                "template_in_progress_state": True,
            }
        )
        self.reassign.action_search()
        self.assertEqual(self.reassign.state, "draft")
        self.assertEqual(len(self.reassign.salesperson_reassign_line_ids), 0)

    def test_crm_salesperson_reassign(self):
        self.reassign.action_search()
        self.reassign.action_validate()
        self.assertEqual(self.reassign.state, "validated")
        self.reassign.action_reassign()
        self.assertEqual(self.reassign.state, "done")
        self.assertRecordValues(self.visit1, [{"user_id": self.salesperson2.id}])
        self.assertRecordValues(self.visit2, [{"user_id": self.salesperson2.id}])

    def test_crm_salesperson_reassign_visits_date_error(self):
        self.reassign.write({"start_date": "2022-01-01", "end_date": "2022-02-28"})
        self.reassign.action_search()
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 2)
        self.reassign.action_validate()
        self.visit1.write({"date": "2021-01-01"})
        with self.assertRaises(ValidationError):
            self.reassign.action_reassign()

    def test_crm_salesperson_reassign_visits_state_error(self):
        self.reassign.action_search()
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 2)
        self.reassign.action_validate()
        self.visit1.write({"state": "cancel"})
        with self.assertRaises(ValidationError):
            self.reassign.action_reassign()

    def test_crm_salesperson_reassign_visits_salesperson_error(self):
        self.reassign.action_search()
        self.assertEqual(len(self.reassign.visit_reassign_line_ids), 2)
        self.reassign.action_validate()
        self.visit1.write({"user_id": self.salesperson2.id})
        with self.assertRaises(ValidationError):
            self.reassign.action_reassign()

    def test_crm_salesperson_reassign_template_state_error(self):
        self.reassign.action_search()
        self.assertEqual(len(self.reassign.salesperson_reassign_line_ids), 1)
        self.reassign.action_validate()
        self.template.write({"state": "cancel"})
        with self.assertRaises(ValidationError):
            self.reassign.action_reassign()

    def test_crm_salesperson_reassign_template_salesperson_error(self):
        self.reassign.action_search()
        self.assertEqual(len(self.reassign.salesperson_reassign_line_ids), 1)
        self.reassign.action_validate()
        self.template.write({"user_id": self.salesperson2.id})
        with self.assertRaises(ValidationError):
            self.reassign.action_reassign()
