# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCrmStage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.crm_lead = cls.env["crm.lead"].create({"name": "Test Lead"})
        cls.stage_new = cls.env.ref("crm.stage_lead1")
        cls.stage_won = cls.env.ref("crm.stage_lead4")

    def test_change_crm_stage_won_without_show_button(self):
        self.stage_new.show_won_button = False
        with self.assertRaises(ValidationError):
            self.crm_lead.stage_id = self.stage_won

    def test_change_crm_stage_to_won_with_show_button(self):
        self.stage_new.show_won_button = True
        self.crm_lead.stage_id = self.stage_won
        self.assertEqual(self.crm_lead.stage_id, self.stage_won)
