# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError

from odoo.tests import common
from odoo.tools import mute_logger


class TestCrmPhoneCallSummaryPredefined(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.summary = cls.env["crm.phonecall.summary"].create({"name": "Test summary"})
        cls.partner = cls.env["res.partner"].create({"name": "Mr Odoo"})
        cls.phonecall = cls.env["crm.phonecall"].create(
            {
                "name": "Test phonecall",
                "partner_id": cls.partner.id,
                "summary_id": cls.summary.id,
            }
        )

    def test_summary_constraint(self):
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.summary.copy()

    def test_schedule_another_phonecall(self):
        new_phonecall = self.phonecall.schedule_another_phonecall(
            {
                "name": "Test schedule method",
                "action": "schedule",
                "summary_id": self.phonecall.summary_id.id,
            }
        )[self.phonecall.id]
        self.assertEqual(new_phonecall.summary_id, self.phonecall.summary_id)

    def test_wizard(self):
        wizard = (
            self.env["crm.phonecall2phonecall"]
            .with_context(
                active_ids=self.phonecall.ids,
                active_id=self.phonecall.id,
                active_model="crm.phonecall",
            )
            .create({})
        )
        self.assertEqual(wizard.summary_id, self.summary)
        result = wizard.action_schedule()
        new_phonecall = self.env["crm.phonecall"].browse(result["res_id"])
        self.assertEqual(new_phonecall.summary_id, self.phonecall.summary_id)
