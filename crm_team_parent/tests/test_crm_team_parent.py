# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.crm_team_parent.models.crm_team import ParentLoopError


class TestCrmTeamParent(TransactionCase):
    def setUp(self):
        super(TestCrmTeamParent, self).setUp()
        self.parent = self.env["crm.team"].create({"name": "Team A"})
        self.child = self.env["crm.team"].create(
            {"name": "Team B", "parent_id": self.parent.id}
        )

    def test_add_child(self):
        grandchild = self.env["crm.team"].create(
            {"name": "Team C", "parent_id": self.child.id}
        )
        self.assertEqual(self.parent, grandchild.parent_id.parent_id)
        self.assertTrue(grandchild in self.child.child_ids)

    def test_hierarchy_loop(self):
        with self.assertRaises(ParentLoopError):
            self.parent.write({"parent_id": self.child.id})
