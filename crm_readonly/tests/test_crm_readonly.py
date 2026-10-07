# Copyright 2026  Akretion (https://www.akretion.com).
# @author Sébastien Alix <sebastien.alix@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import Command
from odoo.exceptions import AccessError

from odoo.addons.base.tests.common import BaseCommon

READONLY_MODELS = {
    "crm.lead",
    "crm.recurring.plan",
    "crm.lead.scoring.frequency",
    "crm.lead.scoring.frequency.field",
    "crm.activity.report",
}


class TestCrmReadonly(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_user = cls.env.ref("base.group_user")
        cls.group_salesman = cls.env.ref("sales_team.group_sale_salesman")
        cls.group_readonly = cls.env.ref("sales_team_readonly.group_sales_readonly")

        cls.user_owner = cls.env["res.users"].create(
            {
                "name": "Lead Owner",
                "login": "crm_readonly_owner",
                "group_ids": [
                    Command.link(cls.group_user.id),
                    Command.link(cls.group_salesman.id),
                ],
            }
        )
        cls.lead = cls.env["crm.lead"].create(
            {"name": "Lead of the Owner", "user_id": cls.user_owner.id}
        )
        cls.lead_unassigned = cls.env["crm.lead"].create({"name": "Lead Unassigned"})

        cls.user_employee = cls.env["res.users"].create(
            {
                "name": "Plain Employee",
                "login": "crm_readonly_employee",
                "group_ids": [Command.link(cls.group_user.id)],
            }
        )
        cls.user_readonly = cls.env["res.users"].create(
            {
                "name": "CRM Readonly",
                "login": "crm_readonly_user",
                "group_ids": [
                    Command.link(cls.group_user.id),
                    Command.link(cls.group_readonly.id),
                ],
            }
        )
        cls.user_salesman = cls.env["res.users"].create(
            {
                "name": "Salesman",
                "login": "crm_readonly_salesman",
                "group_ids": [
                    Command.link(cls.group_user.id),
                    Command.link(cls.group_salesman.id),
                ],
            }
        )
        cls.user_salesman_readonly = cls.env["res.users"].create(
            {
                "name": "Salesman Readonly",
                "login": "crm_readonly_salesman_readonly",
                "group_ids": [
                    Command.link(cls.group_user.id),
                    Command.link(cls.group_salesman.id),
                    Command.link(cls.group_readonly.id),
                ],
            }
        )

    def _lead_ids(self):
        return (self.lead | self.lead_unassigned).ids

    def _visible_leads(self, user):
        return (
            self.env["crm.lead"]
            .with_user(user)
            .search([("id", "in", self._lead_ids())])
        )

    def test_access_rights(self):
        acls = self.env["ir.model.access"].search(
            [
                ("group_id", "=", self.group_readonly.id),
                ("model_id.model", "in", list(READONLY_MODELS)),
            ]
        )
        self.assertEqual({acl.model_id.model for acl in acls}, READONLY_MODELS)
        for acl in acls:
            self.assertEqual(
                (acl.perm_read, acl.perm_write, acl.perm_create, acl.perm_unlink),
                (True, False, False, False),
            )

    def test_readonly_user_can_read_all_leads(self):
        self.assertCountEqual(
            self._visible_leads(self.user_readonly).ids, self._lead_ids()
        )

    def test_salesman_with_readonly_group_reads_all_leads(self):
        self.assertCountEqual(
            self._visible_leads(self.user_salesman_readonly).ids, self._lead_ids()
        )

    def test_salesman_without_readonly_group_cannot_read_foreign_lead(self):
        with self.assertRaises(AccessError):
            self.lead.with_user(self.user_salesman).read(["name"])

    def test_employee_without_group_cannot_read_lead(self):
        with self.assertRaises(AccessError):
            self.lead.with_user(self.user_employee).read(["name"])

    def test_readonly_user_cannot_create_lead(self):
        with self.assertRaises(AccessError):
            self.env["crm.lead"].with_user(self.user_readonly).create(
                {"name": "Sneaky Lead"}
            )

    def test_readonly_user_cannot_write_lead(self):
        with self.assertRaises(AccessError):
            self.lead.with_user(self.user_readonly).write({"name": "Touched"})

    def test_readonly_user_cannot_unlink_lead(self):
        with self.assertRaises(AccessError):
            self.lead.with_user(self.user_readonly).unlink()

    def test_readonly_user_can_read_activities_analysis(self):
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        self.env["mail.message"].create(
            {
                "model": "crm.lead",
                "res_id": self.lead.id,
                "message_type": "notification",
                "mail_activity_type_id": activity_type.id,
                "body": "Done activity on lead",
            }
        )
        report = self.env["crm.activity.report"]
        self.assertTrue(
            report.with_user(self.user_readonly).search(
                [("lead_id", "=", self.lead.id)]
            )
        )
        self.assertTrue(
            report.with_user(self.user_salesman_readonly).search(
                [("lead_id", "=", self.lead.id)]
            )
        )
        self.assertFalse(
            report.with_user(self.user_salesman).search(
                [("lead_id", "=", self.lead.id)]
            )
        )

    def test_menus_visible_for_readonly_user(self):
        visible = (
            self.env["ir.ui.menu"]
            .with_user(self.user_readonly)
            .search([])
            ._filter_visible_menus()
        )
        for xmlid in (
            "crm.crm_menu_root",
            "crm.crm_menu_report",
            "crm.crm_lead_menu_my_activities",
            "crm.menu_crm_opportunities",
        ):
            self.assertIn(self.env.ref(xmlid), visible)
        self.assertNotIn(self.env.ref("crm.crm_menu_config"), visible)

    def test_root_menu_not_visible_for_plain_employee(self):
        visible = (
            self.env["ir.ui.menu"]
            .with_user(self.user_employee)
            .search([])
            ._filter_visible_menus()
        )
        self.assertNotIn(self.env.ref("crm.crm_menu_root"), visible)
