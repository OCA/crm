# Copyright 2025 Teacnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import Command
from odoo.tests import new_test_user, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestCrmStageMultiTeam_NoLeadTeam(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, test_crm_stage_multi_team=True))

        # Cache models
        cls.Team = cls.env["crm.team"]
        cls.Stage = cls.env["crm.stage"]
        cls.Lead = cls.env["crm.lead"]

        # Users (Salesperson A and B)
        cls.user_a = new_test_user(
            cls.env,
            login="sales_a",
            groups="sales_team.group_sale_salesman",
            name="Sales A",
        )
        cls.user_b = new_test_user(
            cls.env,
            login="sales_b",
            groups="sales_team.group_sale_salesman",
            name="Sales B",
        )

        # Teams (no need to assign leads to teams)
        cls.team_a = cls.Team.create({"name": "Team A"})
        cls.team_b = cls.Team.create({"name": "Team B"})

        # Stages: only A, only B, both, global
        cls.stage_only_a = cls.Stage.create(
            {
                "name": "Only A",
                "sequence": 10,
                "team_ids": [Command.set(cls.team_a.ids)],
            }
        )
        cls.stage_only_b = cls.Stage.create(
            {
                "name": "Only B",
                "sequence": 20,
                "team_ids": [Command.set(cls.team_b.ids)],
            }
        )
        cls.stage_both = cls.Stage.create(
            {
                "name": "Both A and B",
                "sequence": 30,
                "team_ids": [Command.set((cls.team_a | cls.team_b).ids)],
            }
        )
        cls.stage_global = cls.Stage.create(
            {
                "name": "Global (no teams)",
                "sequence": 40,
                "team_ids": [Command.clear()],
            }
        )
        cls.custom_stage_ids = {
            cls.stage_only_a.id,
            cls.stage_only_b.id,
            cls.stage_both.id,
            cls.stage_global.id,
        }

        # Leads WITHOUT team_id; set user_id to satisfy record rules
        cls.lead_user_a = cls.Lead.create(
            {
                "name": "Lead (User A, no team)",
                "user_id": cls.user_a.id,
            }
        )
        cls.lead_user_b = cls.Lead.create(
            {
                "name": "Lead (User B, no team)",
                "user_id": cls.user_b.id,
            }
        )

    def test_read_group_stage_ids_users_and_no_team(self):
        """
        Validates _read_group_stage_ids with leads that have NO team_id:
          - If user's crm_team_ids includes Team A → stages for A + Both + Global
          - If user's crm_team_ids includes Team B → stages for B + Both + Global
          - If user has no team → only Global
        """
        empty_stages = self.Stage.browse([])

        # Assign crm_team_ids to users dynamically
        self.user_a.crm_team_ids = [Command.set(self.team_a.ids)]
        self.user_b.crm_team_ids = [Command.set(self.team_b.ids)]

        # Team A user
        stages = self.Lead.with_user(self.user_a)._read_group_stage_ids(
            empty_stages, domain=[]
        )
        self.assertIn(self.stage_only_a, stages)
        self.assertIn(self.stage_both, stages)
        self.assertIn(self.stage_global, stages)
        self.assertNotIn(self.stage_only_b, stages)

        # Team B user
        stages = self.Lead.with_user(self.user_b)._read_group_stage_ids(
            empty_stages, domain=[]
        )
        self.assertIn(self.stage_only_b, stages)
        self.assertIn(self.stage_both, stages)
        self.assertIn(self.stage_global, stages)
        self.assertNotIn(self.stage_only_a, stages)

        # No team assigned → only global stages visible
        self.user_a.crm_team_ids = [Command.clear()]
        stages = self.Lead.with_user(self.user_a)._read_group_stage_ids(
            empty_stages, domain=[]
        )
        self.assertIn(self.stage_global, stages)
        self.assertNotIn(self.stage_only_a, stages)
        self.assertNotIn(self.stage_only_b, stages)
        self.assertNotIn(self.stage_both, stages)

    def test_stage_find_users_no_lead_team(self):
        domain_limit = [("id", "in", list(self.custom_stage_ids))]

        # No team_id param -> should return Global
        stage = self.lead_user_a.with_user(self.user_a)._stage_find(
            domain=domain_limit, order="sequence, id"
        )
        self.assertEqual(stage, self.stage_global)

        stage = self.lead_user_b.with_user(self.user_b)._stage_find(
            domain=domain_limit, order="sequence, id"
        )
        self.assertEqual(stage, self.stage_global)

        # team_id=A -> Only A
        stage = self.lead_user_a.with_user(self.user_a)._stage_find(
            team_id=self.team_a.id, domain=domain_limit, order="sequence, id"
        )
        self.assertEqual(stage, self.stage_only_a)

        # team_id=B -> Only B
        stage = self.lead_user_b.with_user(self.user_b)._stage_find(
            team_id=self.team_b.id, domain=domain_limit, order="sequence, id"
        )
        self.assertEqual(stage, self.stage_only_b)

        # team_id=A + name filter -> Both
        stage = self.lead_user_a.with_user(self.user_a)._stage_find(
            team_id=self.team_a.id,
            domain=domain_limit + [("name", "ilike", "Both")],
            order="sequence, id",
        )
        self.assertEqual(stage, self.stage_both)
