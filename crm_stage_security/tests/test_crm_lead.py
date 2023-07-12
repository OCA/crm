# Copyright 2023 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCrmLead(TransactionCase):
    def setUp(self):
        super().setUp()
        self.lead = self.env["crm.lead"].create({"name": "Test Lead"})
        self.group = self.env["res.groups"].create({"name": "Test Group"})
        self.stage = self.env.ref("crm.stage_lead2")
        self.stage.write({"group_ids": [(4, self.group.id)]})

    def test_check_stage(self):
        with self.assertRaises(ValidationError):
            self.lead.write({"stage_id": self.stage.id})
