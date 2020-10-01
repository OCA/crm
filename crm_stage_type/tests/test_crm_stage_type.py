# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestCrmStageType(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        context = dict(cls.env.context, tracking_disable=True, no_reset_password=True)
        cls.env = cls.env(context=context)
        cls.crm_salemanager = cls.env["res.users"].create(
            {
                "company_id": cls.env.ref("base.main_company").id,
                "name": "Crm Sales manager",
                "login": "csm",
                "email": "crmmanager@yourcompany.com",
                "groups_id": [
                    (6, 0, [cls.env.ref("sales_team.group_sale_manager").id])
                ],
            }
        )
        # archiving default odoo stages is not possible, so change their lead_type
        # and use Won stage for both types
        # Opportunity stages: New => Qualified => Proposition => Won [both]
        # Lead stages: A => B => Won [both]
        cls.env.ref("crm.stage_lead1").write({"lead_type": "opportunity"})
        cls.env.ref("crm.stage_lead2").write({"lead_type": "opportunity"})
        cls.env.ref("crm.stage_lead3").write({"lead_type": "opportunity"})

        Stage = cls.env["crm.stage"]

        cls.lead_stage_a = Stage.create(
            {"name": "A", "lead_type": "lead", "sequence": 4}
        )
        cls.lead_stage_b = Stage.create(
            {"name": "B", "lead_type": "lead", "sequence": 5}
        )
        # freeze stage ids for tests
        cls.stages = [
            cls.env.ref("crm.stage_lead1").id,
            cls.env.ref("crm.stage_lead2").id,
            cls.env.ref("crm.stage_lead3").id,
            cls.lead_stage_a.id,
            cls.lead_stage_b.id,
        ]

        cls.lead = (
            cls.env["crm.lead"]
            .with_context({"default_type": "lead"})
            .create(
                {
                    "type": "lead",
                    "name": "Test lead new",
                    "partner_id": cls.env.ref("base.res_partner_1").id,
                    "description": "This is the description of the test new lead.",
                    "team_id": cls.env.ref("sales_team.team_sales_department").id,
                }
            )
        )

        cls.lead_salesmanager = cls.env["crm.lead"].with_user(cls.crm_salemanager.id)

    def test_read_group_stage_ids(self):
        # test returned stages for lead
        groups_lead = self.lead._read_group_stage_ids(
            self.env["crm.stage"].browse(self.stages), None, "sequence"
        )
        self.assertEqual(
            groups_lead.ids,
            [
                self.lead_stage_a.id,
                self.lead_stage_b.id,
                self.env.ref("crm.stage_lead4").id,
            ],
        )

    def test_find_stage(self):
        self.assertEqual(self.lead.stage_id, self.lead_stage_a)
        self.lead.convert_opportunity(self.env.ref("base.res_partner_2").id)
        self.assertEqual(
            self.lead.stage_id,
            self.env.ref("crm.stage_lead1"),
            "Default stage of converted opportunity is incorrect!",
        )
        self.lead.action_set_won()
        self.assertEqual(self.lead.stage_id, self.env.ref("crm.stage_lead4"))

    def test_crm_lead_merge(self):
        test_crm_opp_01 = self.lead_salesmanager.create(
            {
                "type": "opportunity",
                "name": "Test opportunity 1",
                "partner_id": self.env.ref("base.res_partner_3").id,
                "stage_id": self.env.ref("crm.stage_lead3").id,
                "description": "This is the description of the test opp 1.",
            }
        )
        self.assertEqual(test_crm_opp_01.stage_id, self.env.ref("crm.stage_lead3"))

        self.lead_salesmanager = self.lead_salesmanager.with_context(
            {"default_type": "lead"}
        )

        test_crm_lead_01 = self.lead_salesmanager.create(
            {
                "type": "lead",
                "name": "Test lead first",
                "partner_id": self.env.ref("base.res_partner_1").id,
                "description": "This is the description of the test lead first.",
            }
        )
        self.assertEqual(test_crm_lead_01.stage_id.lead_type, "lead")

        test_crm_lead_02 = self.lead_salesmanager.create(
            {
                "type": "lead",
                "name": "Test lead second",
                "partner_id": self.env.ref("base.res_partner_1").id,
                "description": "This is the description of the test lead second.",
            }
        )

        lead_ids = [
            test_crm_opp_01.id,
            test_crm_lead_01.id,
            test_crm_lead_02.id,
        ]
        add_context = {
            "active_model": "crm.lead",
            "active_ids": lead_ids,
            "active_id": lead_ids[0],
        }

        merge_opp_wizard_01 = (
            self.env["crm.merge.opportunity"]
            .with_user(self.crm_salemanager.id)
            .with_context(**add_context)
            .create({})
        )
        merge_opp_wizard_01.action_merge()

        merged_lead = self.env["crm.lead"].search(
            [
                ("name", "=", "Test opportunity 1"),
                ("partner_id", "=", self.env.ref("base.res_partner_3").id),
            ],
            limit=1,
        )
        self.assertTrue(merged_lead, "Fail to create merge opportunity wizard")
        self.assertEqual(merged_lead.type, "opportunity", "Type mismatch")

        self.assertFalse(
            test_crm_lead_01.exists(), "This tailing lead should not exist anymore"
        )
        self.assertFalse(
            test_crm_lead_02.exists(), "This tailing opp should not exist anymore"
        )
        self.assertEqual(merged_lead.stage_id, self.env.ref("crm.stage_lead3"))
