# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCrmLeadEscalation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.salesperson = cls.env["res.users"].create(
            {
                "name": "Test Salesperson",
                "login": "test_escalation_salesperson",
                "email": "salesperson@test.example.com",
            }
        )
        cls.leader = cls.env["res.users"].create(
            {
                "name": "Test Team Leader",
                "login": "test_escalation_leader",
                "email": "leader@test.example.com",
            }
        )
        cls.director = cls.env["res.users"].create(
            {
                "name": "Test Director",
                "login": "test_escalation_director",
                "email": "director@test.example.com",
            }
        )
        cls.team = cls.env["crm.team"].create(
            {"name": "Test Team", "user_id": cls.leader.id}
        )
        # Rules already in the database would escalate the test leads too.
        cls.env["crm.lead.escalation.rule"].search([]).action_archive()
        cls.rule = cls.env["crm.lead.escalation.rule"].create(
            {
                "name": "Stalled leads",
                "trigger": "no_followup",
                "delay_value": 3,
                "delay_unit": "days",
                "team_ids": [(6, 0, cls.team.ids)],
            }
        )

    def _create_lead(self, **values):
        return self.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "opportunity",
                "user_id": self.salesperson.id,
                "team_id": self.team.id,
                **values,
            }
        )

    def _set_stale(self, lead, days=4):
        lead.last_followup_date = fields.Datetime.now() - timedelta(days=days)

    def _plan_activity(self, lead):
        """A user-planned activity, as the chatter dialog creates it.

        activity_schedule() flags activities as automated, which by design
        does not count as a follow-up.
        """
        return self.env["mail.activity"].create(
            {
                "res_model_id": self.env["ir.model"]._get_id("crm.lead"),
                "res_id": lead.id,
                "activity_type_id": self.env.ref("mail.mail_activity_data_call").id,
                "user_id": self.salesperson.id,
                "summary": "Call the customer",
            }
        )

    def _escalation_mails(self, lead):
        return self.env["mail.mail"].search(
            [
                ("model", "=", "crm.lead"),
                ("res_id", "=", lead.id),
                ("subject", "like", "Lead needs attention%"),
            ]
        )

    def _run_cron(self):
        self.env["crm.lead.escalation.rule"]._cron_escalate_leads()

    def test_fresh_lead_is_not_escalated(self):
        lead = self._create_lead()
        self.assertTrue(lead.last_followup_date)
        self._run_cron()
        self.assertFalse(lead.escalation_rule_ids)

    def test_stale_lead_escalates_to_the_team_leader(self):
        lead = self._create_lead()
        self._set_stale(lead)
        self._run_cron()
        self.assertIn(self.rule, lead.escalation_rule_ids)
        self.assertEqual(lead.activity_ids.user_id, self.leader)
        self.assertIn(
            self.leader.partner_id, self._escalation_mails(lead).recipient_ids
        )
        # A second run must not nag the recipient again.
        self._run_cron()
        self.assertEqual(len(lead.activity_ids), 1)
        self.assertEqual(len(lead.escalation_rule_ids), 1)

    def test_follow_up_after_escalation_allows_a_new_escalation(self):
        lead = self._create_lead()
        self._set_stale(lead)
        self._run_cron()
        lead.message_post(body="Called the customer", message_type="comment")
        self.assertFalse(lead.escalation_rule_ids)
        self._set_stale(lead)
        self._run_cron()
        self.assertIn(self.rule, lead.escalation_rule_ids)

    def test_follow_ups_reset_the_clock(self):
        lead = self._create_lead()
        activity = self._plan_activity(lead)
        stage = self.env["crm.stage"].create({"name": "Qualified"})
        follow_ups = {
            "message": lambda: lead.message_post(
                body="Called the customer", message_type="comment"
            ),
            "planned activity": lambda: self._plan_activity(lead),
            "completed activity": activity.action_done,
            "stage change": lambda: lead.write({"stage_id": stage.id}),
            "salesperson change": lambda: lead.write({"user_id": self.leader.id}),
        }
        for name, follow_up in follow_ups.items():
            with self.subTest(follow_up=name):
                self._set_stale(lead)
                stale_date = lead.last_followup_date
                follow_up()
                self.assertGreater(lead.last_followup_date, stale_date)
        self._run_cron()
        self.assertFalse(lead.escalation_rule_ids)

    def test_non_follow_up_events_do_not_reset_the_clock(self):
        lead = self._create_lead()
        self._set_stale(lead)
        stale_date = lead.last_followup_date
        lead.write({"user_id": lead.user_id.id})
        self.assertEqual(
            lead.last_followup_date, stale_date, "Rewriting the same value."
        )
        self.env["mail.activity"].create(
            {
                "res_model_id": self.env["ir.model"]._get_id("crm.lead"),
                "res_id": lead.id,
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                "user_id": self.salesperson.id,
                "summary": "Automated reminder",
                "automated": True,
            }
        )
        self.assertEqual(lead.last_followup_date, stale_date, "An automated activity.")
        self._run_cron()
        self.assertEqual(lead.last_followup_date, stale_date, "The escalation itself.")

    def test_assign_recipient_changes_the_salesperson(self):
        self.rule.assign_recipient = True
        lead = self._create_lead()
        self._set_stale(lead)
        self._run_cron()
        self.assertEqual(lead.user_id, self.leader)
        self.assertIn(
            self.rule,
            lead.escalation_rule_ids,
            "The reassignment must not reset the escalation.",
        )

    def test_not_closed_rule_notifies_specific_user(self):
        self.rule.active = False
        rule = self.env["crm.lead.escalation.rule"].create(
            {
                "name": "Not closed in 4 hours",
                "trigger": "not_closed",
                "delay_value": 4,
                "delay_unit": "hours",
                "recipient_type": "user",
                "recipient_user_id": self.director.id,
            }
        )
        lead = self._create_lead()
        lead.create_date = fields.Datetime.now() - timedelta(hours=5)
        self._run_cron()
        self.assertIn(rule, lead.escalation_rule_ids)
        self.assertEqual(lead.activity_ids.user_id, self.director)

    def test_recipient_user_is_required(self):
        with self.assertRaises(ValidationError):
            self.env["crm.lead.escalation.rule"].create(
                {"name": "Broken", "recipient_type": "user"}
            )

    def test_closed_leads_are_not_escalated(self):
        won_stage = self.env["crm.stage"].create({"name": "Won", "is_won": True})
        won_lead = self._create_lead(stage_id=won_stage.id)
        lost_lead = self._create_lead()
        lost_lead.action_set_lost()
        for lead in won_lead + lost_lead:
            self._set_stale(lead)
        self._run_cron()
        self.assertFalse(won_lead.escalation_rule_ids)
        self.assertFalse(lost_lead.escalation_rule_ids)

    def test_rule_filters_exclude_non_matching_leads(self):
        other_team = self.env["crm.team"].create(
            {"name": "Other Team", "user_id": self.leader.id}
        )
        other_team_lead = self._create_lead(team_id=other_team.id)
        unassigned_lead = self._create_lead(user_id=False)
        for lead in other_team_lead + unassigned_lead:
            self._set_stale(lead)
        self._run_cron()
        self.assertFalse(other_team_lead.escalation_rule_ids, "Another sales team.")
        self.assertFalse(unassigned_lead.escalation_rule_ids, "No salesperson.")
        self.rule.lead_type = "lead"
        opportunity = self._create_lead()
        self._set_stale(opportunity)
        self._run_cron()
        self.assertFalse(
            opportunity.escalation_rule_ids,
            "An opportunity must not match a lead rule.",
        )

    def test_no_mail_without_template(self):
        self.rule.mail_template_id = False
        lead = self._create_lead()
        self._set_stale(lead)
        self._run_cron()
        self.assertIn(self.rule, lead.escalation_rule_ids)
        self.assertFalse(self._escalation_mails(lead))

    def test_unreachable_recipient_does_not_starve_the_queue(self):
        """Leads that yield no recipient must not come back on every run."""
        self.leader.action_archive()
        archived_leader_lead = self._create_lead()
        self._set_stale(archived_leader_lead)
        self._run_cron()
        self.assertFalse(archived_leader_lead.activity_ids)
        self.assertIn(self.rule, archived_leader_lead.escalation_rule_ids)
        # Without any leader at all, the domain already excludes the lead.
        self.team.user_id = False
        leaderless_lead = self._create_lead()
        self._set_stale(leaderless_lead)
        self._run_cron()
        self.assertFalse(leaderless_lead.escalation_rule_ids)

    def test_escalation_is_batched_per_recipient(self):
        leads = self.env["crm.lead"]
        for index in range(5):
            lead = self._create_lead(name=f"Lead {index}")
            self._set_stale(lead)
            leads |= lead
        with self.assertQueryCount(__system__=125):
            self._run_cron()
        self.assertEqual(len(leads.escalation_rule_ids), 1)
        self.assertEqual(len(leads.activity_ids), 5)
