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

        cls.crm_lead = cls.env["crm.lead"].create(
            {"name": "Test Lead", "type": "opportunity", "user_id": cls.env.user.id}
        )

        cls.mail_activity = cls.env["mail.activity"].search(
            [
                ("res_id", "=", cls.crm_lead.id),
                ("res_model", "=", "crm.lead"),
                ("res_name", "=", cls.crm_lead.name),
            ]
        )

    def test_new_automated_activity(self):

        self.assertIn(self.mail_activity.id, self.crm_lead.activity_ids.ids)
