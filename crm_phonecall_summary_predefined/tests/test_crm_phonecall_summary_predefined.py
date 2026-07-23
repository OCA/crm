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
        """Duplicate summary names must raise an IntegrityError."""
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.env["crm.phonecall.summary"].create({"name": self.summary.name})

    def test_summary_name_stored_related(self):
        """The phonecall name (stored-related) equals the summary name."""
        self.assertEqual(self.phonecall.name, self.summary.name)

    def test_summary_phonecall_ids_inverse(self):
        """phonecall_ids on the summary correctly reflects linked phonecalls."""
        self.assertIn(self.phonecall, self.summary.phonecall_ids)

    def test_summary_phonecall_ids_multiple(self):
        """Multiple phonecalls linked to the same summary appear in phonecall_ids."""
        second_call = self.env["crm.phonecall"].create(
            {
                "name": "Second call",
                "partner_id": self.partner.id,
                "summary_id": self.summary.id,
            }
        )
        self.assertIn(self.phonecall, self.summary.phonecall_ids)
        self.assertIn(second_call, self.summary.phonecall_ids)

    def test_schedule_another_phonecall(self):
        """schedule_another_phonecall propagates summary_id when present in vals."""
        new_phonecall = self.phonecall.schedule_another_phonecall(
            {
                "name": "Test schedule method",
                "action": "schedule",
                "summary_id": self.phonecall.summary_id.id,
            }
        )[self.phonecall.id]
        self.assertEqual(new_phonecall.summary_id, self.phonecall.summary_id)

    def test_schedule_another_phonecall_without_summary_id(self):
        """get_values_schedule_another_phonecall with no summary_id in vals
        must still return the key with a falsy (None) value and not raise.
        """
        vals = self.phonecall.get_values_schedule_another_phonecall(
            {"name": "No summary", "action": "schedule"}
        )
        self.assertIn("summary_id", vals)
        self.assertFalse(vals["summary_id"])

    def test_schedule_another_phonecall_different_summary(self):
        """schedule_another_phonecall uses the summary_id explicitly supplied."""
        other_summary = self.env["crm.phonecall.summary"].create(
            {"name": "Another summary"}
        )
        new_phonecall = self.phonecall.schedule_another_phonecall(
            {
                "name": "Different summary call",
                "action": "schedule",
                "summary_id": other_summary.id,
            }
        )[self.phonecall.id]
        self.assertEqual(new_phonecall.summary_id, other_summary)

    def _make_wizard(self, extra_context=None):
        ctx = {
            "active_ids": self.phonecall.ids,
            "active_id": self.phonecall.id,
            "active_model": "crm.phonecall",
        }
        if extra_context:
            ctx.update(extra_context)
        return self.env["crm.phonecall2phonecall"].with_context(**ctx).create({})

    def test_wizard(self):
        """Wizard default_get fills summary_id; action_schedule propagates it."""
        wizard = self._make_wizard()
        self.assertEqual(wizard.summary_id, self.summary)
        result = wizard.action_schedule()
        new_phonecall = self.env["crm.phonecall"].browse(result["res_id"])
        self.assertEqual(new_phonecall.summary_id, self.phonecall.summary_id)

    def test_wizard_get_vals_action_schedule_includes_summary_id(self):
        """get_vals_action_schedule must return the summary_id key."""
        wizard = self._make_wizard()
        vals = wizard.get_vals_action_schedule()
        self.assertIn("summary_id", vals)
        self.assertEqual(vals["summary_id"], self.summary.id)

    def test_wizard_name_related_to_summary(self):
        """Wizard name field (stored-related) matches summary_id.name."""
        wizard = self._make_wizard()
        self.assertEqual(wizard.name, self.summary.name)

    def test_wizard_default_get_non_phonecall_model(self):
        """When active_model != 'crm.phonecall', the summary_id auto-fill
        branch is skipped; the wizard is still created with an explicit value.
        """
        wizard = (
            self.env["crm.phonecall2phonecall"]
            .with_context(
                active_ids=self.phonecall.ids,
                active_id=self.phonecall.id,
                active_model="res.partner",
            )
            .create({"summary_id": self.summary.id})
        )
        self.assertEqual(wizard.summary_id, self.summary)

    def test_wizard_action_schedule_log_action(self):
        """Wizard with action='log' also propagates summary_id correctly."""
        wizard = self._make_wizard()
        wizard.action = "log"
        result = wizard.action_schedule()
        new_phonecall = self.env["crm.phonecall"].browse(result["res_id"])
        self.assertEqual(new_phonecall.summary_id, self.phonecall.summary_id)
