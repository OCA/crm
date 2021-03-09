# Copyright 2021 Tecnativa - Víctor Martínez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from psycopg2 import IntegrityError

from odoo.tests import Form, common
from odoo.tools import mute_logger


class TestCrmProject(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.user_demo = cls.env.ref("base.user_demo")

    def test_crm_with_distinct_secondary_user_id(self):
        lead = Form(self.env["crm.lead"])
        lead.name = "Test"
        lead.user_id = self.user_admin
        lead.secondary_user_id = self.user_demo
        lead = lead.save()
        self.assertEqual(lead.secondary_user_id, self.user_demo)

    def test_crm_with_equal_secondary_user_id(self):
        lead = Form(self.env["crm.lead"])
        lead.name = "Test"
        lead.user_id = self.user_admin
        lead.secondary_user_id = self.user_admin
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            lead.save()
