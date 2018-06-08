# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase


class TestCrmLeadProject(TransactionCase):

    def setUp(self):
        super(TestCrmLeadProject, self).setUp()
        self.lead = self.env.ref('crm.crm_case_1')

    def test_convert_create_project(self):
        wiz = self.env['crm.lead2opportunity.partner'].with_context(
            active_id=self.lead.id, active_ids=self.lead.ids).create({})
        wiz.name = 'convert_create_project'
        wiz.action_apply()
        self.assertTrue(self.lead.project_id)
        self.assertTrue(self.lead.project_id.use_tasks)
        self.assertTrue(self.lead.project_id.crm_project)
        self.assertEqual(self.lead.project_id.lead_id, self.lead)
        self.assertEqual(self.lead.project_id.name, self.lead.name)
