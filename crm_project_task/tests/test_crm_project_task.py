# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.mail.tests.common import mail_new_test_user


@tagged("post_install", "-at_install")
class TestCrmProjectTask(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.user.company_id
        cls.company_2 = cls.env["res.company"].create({"name": "Second Company"})
        cls.user_salesman = mail_new_test_user(
            cls.env,
            login="user_test",
            name="User Test",
            email="user_test@test.example.com",
            company_id=cls.company.id,
            groups="sales_team.group_sale_salesman",
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner Test"})
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "lead",
                "partner_id": cls.partner.id,
                "user_id": cls.user_salesman.id,
            }
        )
        cls.lead_2 = cls.env["crm.lead"].create(
            {
                "name": "Other Lead",
                "type": "lead",
                "company_id": cls.company_2.id,
            }
        )
        cls.project = cls.env["project.project"].create(
            {"name": "Test Project", "description": "Test Description"}
        )
        cls.project_2 = cls.env["project.project"].create(
            {"name": "Second Project", "description": "Second Description"}
        )
        cls.company.crm_default_project_id = cls.project

    @classmethod
    def _new_project_user(cls, login, **kwargs):
        return mail_new_test_user(
            cls.env,
            login=login,
            company_id=cls.company.id,
            groups="sales_team.group_sale_salesman,project.group_project_user",
            **kwargs,
        )

    def _wizard(self, user=None, lead=None, **values):
        user = user or self.user_salesman
        lead = lead or self.lead
        return (
            self.env["crm.create.task"]
            .with_user(user)
            .create({"lead_id": lead.id, **values})
        )

    def _assert_task_action_context(self, action, lead, project, assignee):
        self.assertEqual(action["context"]["default_name"], lead.name)
        self.assertEqual(action["context"]["default_lead_id"], lead.id)
        self.assertEqual(action["context"]["default_project_id"], project.id)
        self.assertEqual(action["context"]["default_partner_id"], lead.partner_id.id)
        self.assertEqual(
            action["context"]["default_user_ids"],
            [fields.Command.set(assignee.ids)],
        )

    # -- Default project resolution --------------------------------------------

    def test_get_crm_default_project_prefers_lead_company(self):
        self.company_2.crm_default_project_id = self.project_2
        self.company.crm_default_project_id = self.project

        self.assertEqual(self.lead_2._get_crm_default_project(), self.project_2)
        self.assertEqual(self.lead._get_crm_default_project(), self.project)

    def test_get_default_context_matches_default_project(self):
        self.company_2.crm_default_project_id = self.project_2

        context = self.lead_2._get_default_context()

        self.assertEqual(context["default_project_id"], self.project_2.id)

    # -- _can_create_task_natively ---------------------------------------------

    def test_can_create_task_natively_requires_project_user(self):
        self.assertFalse(
            self.lead.with_user(self.user_salesman)._can_create_task_natively()
        )

    def test_can_create_task_natively_true_for_project_user(self):
        project_user = self._new_project_user(
            "user_native_check",
            name="Native Check User",
            email="native_check@test.example.com",
        )
        self.lead.user_id = project_user
        self.assertTrue(self.lead.with_user(project_user)._can_create_task_natively())

    # -- action_create_task ----------------------------------------------------

    def test_action_create_task_native_form_for_project_user(self):
        project_user = self._new_project_user(
            "user_project", name="Project User", email="user_project@test.example.com"
        )
        self.lead.user_id = project_user
        action = self.lead.with_user(project_user).action_create_task()

        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(action["view_mode"], "form")
        self._assert_task_action_context(action, self.lead, self.project, project_user)

    def test_action_create_task_wizard_for_salesman(self):
        action = self.lead.with_user(self.user_salesman).action_create_task()

        self.assertEqual(action["res_model"], "crm.create.task")
        self.assertEqual(action.get("target"), "new")
        self._assert_task_action_context(
            action, self.lead, self.project, self.user_salesman
        )

    def test_action_create_task_raises_without_default_project(self):
        self.company.crm_default_project_id = False
        with self.assertRaises(UserError):
            self.lead.action_create_task()

    # -- action_view_tasks -----------------------------------------------------

    def test_action_view_tasks_domain_and_context(self):
        task = self.env["project.task"].create(
            {
                "name": "Task Test",
                "lead_id": self.lead.id,
                "project_id": self.project.id,
            }
        )
        action = self.lead.action_view_tasks()

        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(action["context"]["search_default_open_tasks"], 1)
        self._assert_task_action_context(
            action, self.lead, self.project, self.user_salesman
        )
        self.assertEqual(list(action["domain"]), [("lead_id", "=", self.lead.id)])
        self.assertIn(task, self.env["project.task"].search(action["domain"]))

    def test_action_view_tasks_disables_create_without_native_rights(self):
        self.env["project.task"].create(
            {
                "name": "Task Test",
                "lead_id": self.lead.id,
                "project_id": self.project.id,
            }
        )
        action = self.lead.with_user(self.user_salesman).action_view_tasks()
        self.assertFalse(action["context"]["create"])

    def test_action_view_tasks_keeps_create_for_project_user(self):
        project_user = self._new_project_user(
            "user_project_view",
            name="Project View User",
            email="user_project_view@test.example.com",
        )
        self.lead.user_id = project_user
        action = self.lead.with_user(project_user).action_view_tasks()
        self.assertNotIn("create", action["context"])

    # -- Wizard create_task ----------------------------------------------------

    def test_wizard_create_task_creates_linked_task(self):
        self._wizard(task_name="Wizard Task", description="<p>Desc</p>").create_task()
        task = self.env["project.task"].search(
            [("lead_id", "=", self.lead.id), ("name", "=", "Wizard Task")]
        )
        self.assertEqual(len(task), 1)
        self.assertEqual(task.project_id, self.project)
        self.assertEqual(task.partner_id, self.partner)
        self.assertEqual(task.description, "<p>Desc</p>")
        self.assertFalse(task.user_ids)

    def test_wizard_uses_lead_company_default_project(self):
        self.company_2.crm_default_project_id = self.project_2
        wizard = self.env["crm.create.task"].create(
            {"lead_id": self.lead_2.id, "task_name": "Cross Company Task"}
        )
        wizard.create_task()
        task = self.env["project.task"].search(
            [("lead_id", "=", self.lead_2.id), ("name", "=", "Cross Company Task")]
        )
        self.assertEqual(task.project_id, self.project_2)

    def test_wizard_create_task_unsubscribes_only_creator(self):
        private_project = self.env["project.project"].create(
            {"name": "Private CRM Project", "privacy_visibility": "followers"}
        )
        self.company.crm_default_project_id = private_project
        other_follower = self.env["res.partner"].create({"name": "Other Follower"})
        self._wizard(task_name="Private Wizard Task").create_task()
        task = self.env["project.task"].search(
            [("lead_id", "=", self.lead.id), ("name", "=", "Private Wizard Task")]
        )
        task.message_subscribe(other_follower.ids)
        self.assertNotIn(self.user_salesman.partner_id, task.message_partner_ids)
        self.assertIn(other_follower, task.message_partner_ids)
        with self.assertRaises(AccessError):
            task.with_user(self.user_salesman).read(["name"])

    def test_wizard_create_task_raises_without_default_project(self):
        self.company.crm_default_project_id = False
        with self.assertRaises(UserError):
            self._wizard(task_name="No Project").create_task()

    # -- Other model extensions ------------------------------------------------

    def test_task_count_computed_from_related_tasks(self):
        self.assertEqual(self.lead.task_count, 0)
        self.env["project.task"].create(
            {"name": "Task 1", "lead_id": self.lead.id, "project_id": self.project.id}
        )
        self.env["project.task"].create(
            {"name": "Task 2", "lead_id": self.lead.id, "project_id": self.project.id}
        )
        self.lead.invalidate_recordset(["task_ids", "task_count"])
        self.assertEqual(self.lead.task_count, 2)

    def test_merge_get_fields_specific_keeps_tasks_linked(self):
        task_1 = self.env["project.task"].create(
            {
                "name": "Merge Task 1",
                "lead_id": self.lead.id,
                "project_id": self.project.id,
            }
        )
        task_2 = self.env["project.task"].create(
            {
                "name": "Merge Task 2",
                "lead_id": self.lead.id,
                "project_id": self.project.id,
            }
        )
        fields_info = self.lead._merge_get_fields_specific()
        task_commands = fields_info["task_ids"]("task_ids", self.lead)
        linked_ids = {command[1] for command in task_commands if command[0] == 4}
        self.assertSetEqual(linked_ids, {task_1.id, task_2.id})

    def test_res_config_settings_related_default_project(self):
        settings = self.env["res.config.settings"].create(
            {"company_id": self.company.id}
        )
        self.assertEqual(settings.crm_default_project_id, self.project)
        settings.crm_default_project_id = self.project_2
        self.assertEqual(self.company.crm_default_project_id, self.project_2)

    def test_action_open_parent_lead(self):
        task = self.env["project.task"].create(
            {
                "name": "Task linked to lead",
                "lead_id": self.lead.id,
                "project_id": self.project.id,
            }
        )
        action = task.action_open_parent_lead()
        self.assertEqual(action["res_model"], "crm.lead")
        self.assertEqual(action["res_id"], self.lead.id)
