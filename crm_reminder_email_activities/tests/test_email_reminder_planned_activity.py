from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests.common import TransactionCase, new_test_user


class TestEmailReminderPlannedActivity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_a = new_test_user(
            cls.env,
            login="user_a",
            name="Reminder User A",
            groups="base.group_user,sales_team.group_sale_salesman",
        )
        cls.user_b = new_test_user(
            cls.env,
            login="user_b",
            name="Reminder User B",
            groups="base.group_user,sales_team.group_sale_salesman",
        )

        cls.activity_type = cls.env.ref("mail.mail_activity_data_todo")

        cls.lead_1 = cls.env["crm.lead"].create(
            {
                "name": "Reminder Lead 1",
                "type": "opportunity",
            }
        )
        cls.lead_2 = cls.env["crm.lead"].create(
            {
                "name": "Reminder Lead 2",
                "type": "opportunity",
            }
        )

        cls.today = fields.Date.context_today(cls.env.user)

    def _create_activity(self, lead, user, deadline):
        return self.env["mail.activity"].create(
            {
                "res_model_id": self.env.ref("crm.model_crm_lead").id,
                "res_id": lead.id,
                "activity_type_id": self.activity_type.id,
                "user_id": user.id,
                "date_deadline": deadline,
            }
        )

    def test_get_crm_activities_date_boundaries(self):
        """Check that the `_get_crm_activities` function
        selects the right activities related to the correct user
        """
        # Correct
        act_today = self._create_activity(self.lead_1, self.user_a, self.today)
        act_day7 = self._create_activity(
            self.lead_1, self.user_a, self.today + relativedelta(days=7)
        )

        # Not correct
        act_day8 = self._create_activity(
            self.lead_1, self.user_a, self.today + relativedelta(days=8)
        )
        act_yesterday = self._create_activity(
            self.lead_1, self.user_a, self.today - relativedelta(days=1)
        )
        act_today_user_b = self._create_activity(self.lead_1, self.user_b, self.today)
        act_day8_user_b = self._create_activity(
            self.lead_1, self.user_b, self.today + relativedelta(days=8)
        )

        result = self.env["res.users"]._get_crm_activities(user=self.user_a)

        self.assertIn(act_today, result)
        self.assertIn(act_day7, result)
        self.assertNotIn(act_day8, result)
        self.assertNotIn(act_yesterday, result)
        self.assertNotIn(act_today_user_b, result)
        self.assertNotIn(act_day8_user_b, result)
        self.assertEqual(len(result), 2)

    def test_get_crm_activities_filters_res_model(self):
        """Check that function `_get_crm_activities`
        correctly checks the res_model of the activity
        """
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        partner_activity = self.env["mail.activity"].create(
            {
                "res_model_id": self.env.ref("base.model_res_partner").id,
                "res_id": partner.id,
                "activity_type_id": self.activity_type.id,
                "user_id": self.user_a.id,
                "date_deadline": self.today,
            }
        )

        lead_activity = self._create_activity(self.lead_1, self.user_a, self.today)

        result = self.env["res.users"]._get_crm_activities(user=self.user_a)

        self.assertIn(lead_activity, result)
        self.assertNotIn(partner_activity, result)
        self.assertEqual(len(result), 1)

    def test_get_crm_activities_without_user(self):
        """Check that function `_get_crm_activities` works
        correctly even without specifying a specific user
        """
        act_in = self._create_activity(self.lead_1, self.user_a, self.today)
        act_out = self._create_activity(
            self.lead_1, self.user_b, self.today + relativedelta(days=8)
        )

        result = self.env["res.users"]._get_crm_activities()

        self.assertIn(act_in, result)
        self.assertNotIn(act_out, result)
