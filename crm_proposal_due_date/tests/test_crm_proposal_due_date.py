# Copyright 2026 Ctrl-a
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestCrmProposalDueDate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.activity_type = cls.env.ref(
            "crm_proposal_due_date.mail_activity_type_proposal"
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "opportunity",
            }
        )

    def _get_proposal_activities(self, lead):
        return lead.activity_ids.filtered(
            lambda a: a.activity_type_id == self.activity_type and a.automated
        )

    def test_no_activity_without_due_date(self):
        """No proposal activity should exist when proposal_due_date is not set."""
        self.assertFalse(self.lead.proposal_due_date)
        self.assertFalse(self._get_proposal_activities(self.lead))

    def test_activity_created_on_date_set(self):
        """Setting proposal_due_date for the first time schedules a proposal activity."""
        due = date.today() + timedelta(days=7)
        self.lead.write({"proposal_due_date": due})
        activities = self._get_proposal_activities(self.lead)
        self.assertEqual(len(activities), 1)

    def test_activity_created_on_create_with_date(self):
        """Creating a lead with proposal_due_date immediately schedules the activity."""
        due = date.today() + timedelta(days=14)
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead with due date",
                "type": "opportunity",
                "proposal_due_date": due,
            }
        )
        activities = self._get_proposal_activities(lead)
        self.assertEqual(len(activities), 1)

    def test_no_duplicate_activity_on_date_change(self):
        """Changing proposal_due_date does not create a second activity."""
        due1 = date.today() + timedelta(days=7)
        due2 = date.today() + timedelta(days=14)
        self.lead.write({"proposal_due_date": due1})
        self.lead.write({"proposal_due_date": due2})
        activities = self._get_proposal_activities(self.lead)
        self.assertEqual(len(activities), 1)

    def test_activity_removed_on_date_cleared(self):
        """Clearing proposal_due_date removes the proposal activity."""
        due = date.today() + timedelta(days=7)
        self.lead.write({"proposal_due_date": due})
        self.assertTrue(self._get_proposal_activities(self.lead))
        self.lead.write({"proposal_due_date": False})
        self.assertFalse(self._get_proposal_activities(self.lead))

    def test_no_activity_for_write_without_date_change(self):
        """Writing unrelated fields does not create a spurious activity."""
        initial_count = len(self.lead.activity_ids)
        self.lead.write({"name": "Updated Lead Name"})
        self.assertEqual(len(self.lead.activity_ids), initial_count)
