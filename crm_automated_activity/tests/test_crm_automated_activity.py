# Copyright 2021 Pingo Tecnologia - Éder Brito
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAutomatedActivity(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAutomatedActivity, cls).setUpClass()

        cls.activity_type = cls.env.ref("mail.mail_activity_data_call")

        cls.crm_stage = cls.env["crm.stage"].create({"name": "Test Stage"})

        cls.automated_activity = cls.env["automated.activity"].create(
            {
                "crm_stage_id": cls.crm_stage.id,
                "apply_in": "create",
                "activity_type_id": cls.activity_type.id,
                "summary": "Test Automated Activity",
                "days_deadline": "3",
                "note": "Note",
            }
        )

    def test_new_automated_activity(self):
        crm_lead = self.env["crm.lead"].create(
            {"name": "Test Lead", "type": "opportunity", "user_id": self.env.user.id}
        )

        mail_activity = self.env["mail.activity"].search(
            [
                ("res_id", "=", crm_lead.id),
                ("res_model", "=", "crm.lead"),
                ("res_name", "=", crm_lead.name),
            ]
        )

        self.assertIn(mail_activity.id, crm_lead.activity_ids)
