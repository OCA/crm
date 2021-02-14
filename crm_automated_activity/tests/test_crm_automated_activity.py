# Copyright 2021 Pingo Tecnologia - Éder Brito
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAutomatedActivity(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAutomatedActivity, cls).setUpClass()

        cls.activity_type = cls.env.ref("mail.mail_activity_data_call")

        cls.crm_automated_acitivy = cls.env["crm.automated.activity"].create(
            {
                "apply_in": "create",
                "activity_type_id": cls.activity_type.id,
                "summary": "Test Automated Activity",
                "days_deadline": 3,
            }
        )

        cls.crm_automated_acitivy._onchange_activity_type()

        cls.crm_stage = cls.env["crm.stage"].create(
            {
                "name": "Test Stage",
                "create_automated_activity": True,
                "automated_activity_ids": [(4, cls.crm_automated_acitivy.id, 0)],
            }
        )

        cls.crm_lead = cls.env["crm.lead"].create(
            {
                "name": "Test Lead",
                "type": "opportunity",
                "stage_id": cls.crm_stage.id,
                "user_id": cls.env.user.id,
            }
        )

    def test_new_automated_activity(self):

        self.assertTrue(self.activity_type)

        self.assertTrue(self.crm_stage)

        self.assertTrue(self.crm_lead)

        self.assertTrue(self.crm_stage.automated_activity_ids)
