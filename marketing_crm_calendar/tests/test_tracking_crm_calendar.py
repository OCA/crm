from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestTrackingCrmCalendar(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.campaign = cls.env["utm.campaign"].create({"name": "Facebook Campaign"})
        cls.source = cls.env["utm.source"].create({"name": "Facebook"})
        cls.medium = cls.env["utm.medium"].create({"name": "Social Media"})

        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner", "phone": "+34666777888"}
        )

        cls.phonecall_with_marketing = cls.env["crm.phonecall"].create(
            {
                "name": "Test Phone Call with Marketing",
                "partner_id": cls.partner.id,
                "campaign_id": cls.campaign.id,
                "source_id": cls.source.id,
                "medium_id": cls.medium.id,
            }
        )

        cls.phonecall_without_marketing = cls.env["crm.phonecall"].create(
            {"name": "Test Phone Call without Marketing", "partner_id": cls.partner.id}
        )

    def test_calendar_event_without_phonecall_context(self):
        """Calendar event created without call context should not copy fields."""
        event = self.env["calendar.event"].create(
            {
                "name": "Test Event Without Context",
                "start": "2025-07-30 10:00:00",
                "stop": "2025-07-30 11:00:00",
            }
        )

        self.assertFalse(event.campaign_id)
        self.assertFalse(event.source_id)
        self.assertFalse(event.medium_id)
        self.assertFalse(event.phonecall_id)

    def test_calendar_event_with_phonecall_context_and_marketing(self):
        """Event created from call context should copy marketing fields."""
        context = {
            "active_model": "crm.phonecall",
            "active_id": self.phonecall_with_marketing.id,
            "active_ids": [self.phonecall_with_marketing.id],
        }

        event = (
            self.env["calendar.event"]
            .with_context(**context)
            .create(
                {
                    "name": "Test Event From Phonecall",
                    "start": "2025-07-30 10:00:00",
                    "stop": "2025-07-30 11:00:00",
                }
            )
        )

        self.assertEqual(event.campaign_id, self.campaign)
        self.assertEqual(event.source_id, self.source)
        self.assertEqual(event.medium_id, self.medium)
        self.assertEqual(event.phonecall_id, self.phonecall_with_marketing)

    def test_calendar_event_with_phonecall_context_without_marketing(self):
        """Event created from call without marketing should only assign phonecall_id."""
        context = {
            "active_model": "crm.phonecall",
            "active_id": self.phonecall_without_marketing.id,
            "active_ids": [self.phonecall_without_marketing.id],
        }

        event = (
            self.env["calendar.event"]
            .with_context(**context)
            .create(
                {
                    "name": "Test Event From Phonecall Without Marketing",
                    "start": "2025-07-30 10:00:00",
                    "stop": "2025-07-30 11:00:00",
                }
            )
        )

        self.assertFalse(event.campaign_id)
        self.assertFalse(event.source_id)
        self.assertFalse(event.medium_id)
        self.assertEqual(event.phonecall_id, self.phonecall_without_marketing)

    def test_calendar_event_with_wrong_context_model(self):
        """Event with incorrect context model should not copy fields."""
        context = {
            "active_model": "crm.lead",
            "active_id": self.phonecall_with_marketing.id,
        }

        event = (
            self.env["calendar.event"]
            .with_context(**context)
            .create(
                {
                    "name": "Test Event Wrong Context",
                    "start": "2025-07-30 10:00:00",
                    "stop": "2025-07-30 11:00:00",
                }
            )
        )

        self.assertFalse(event.campaign_id)
        self.assertFalse(event.source_id)
        self.assertFalse(event.medium_id)
        self.assertFalse(event.phonecall_id)

    def test_calendar_event_with_invalid_phonecall_id(self):
        """Event with non-existent call ID should not fail."""
        context = {"active_model": "crm.phonecall", "active_id": 99999}

        event = (
            self.env["calendar.event"]
            .with_context(**context)
            .create(
                {
                    "name": "Test Event Invalid Phonecall",
                    "start": "2025-07-30 10:00:00",
                    "stop": "2025-07-30 11:00:00",
                }
            )
        )

        self.assertFalse(event.campaign_id)
        self.assertFalse(event.source_id)
        self.assertFalse(event.medium_id)
        self.assertFalse(event.phonecall_id)

    def test_calendar_event_multiple_create(self):
        """Multiple created events should correctly handle context."""
        context = {
            "active_model": "crm.phonecall",
            "active_id": self.phonecall_with_marketing.id,
        }

        vals_list = [
            {
                "name": "Event 1",
                "start": "2025-07-30 10:00:00",
                "stop": "2025-07-30 11:00:00",
            },
            {
                "name": "Event 2",
                "start": "2025-07-30 14:00:00",
                "stop": "2025-07-30 15:00:00",
            },
        ]

        events = self.env["calendar.event"].with_context(**context).create(vals_list)

        for event in events:
            self.assertEqual(event.campaign_id, self.campaign)
            self.assertEqual(event.source_id, self.source)
            self.assertEqual(event.medium_id, self.medium)
            self.assertEqual(event.phonecall_id, self.phonecall_with_marketing)

    def test_calendar_event_partial_marketing_fields(self):
        """Call with only some marketing fields should copy only existing ones."""
        phonecall_partial = self.env["crm.phonecall"].create(
            {
                "name": "Partial Marketing Call",
                "partner_id": self.partner.id,
                "campaign_id": self.campaign.id,
            }
        )

        context = {"active_model": "crm.phonecall", "active_id": phonecall_partial.id}

        event = (
            self.env["calendar.event"]
            .with_context(**context)
            .create(
                {
                    "name": "Test Partial Marketing",
                    "start": "2025-07-30 10:00:00",
                    "stop": "2025-07-30 11:00:00",
                }
            )
        )

        self.assertEqual(event.campaign_id, self.campaign)
        self.assertFalse(event.source_id)
        self.assertFalse(event.medium_id)
        self.assertEqual(event.phonecall_id, phonecall_partial)
