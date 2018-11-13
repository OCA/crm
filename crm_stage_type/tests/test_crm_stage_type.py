# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestCrmStageType(TransactionCase):
    def setUp(self):
        super(TestCrmStageType, self).setUp()

        self.crm_salemanager = self.env['res.users'].create({
            'company_id': self.env.ref("base.main_company").id,
            'name': "Crm Sales manager",
            'login': "csm",
            'email': "crmmanager@yourcompany.com",
            'groups_id': [(6, 0, [self.ref('sales_team.group_sale_manager')])]
        })

    def test_find_stage(self):
        lead = self.env['crm.lead'].create({
            'type': "lead",
            'name': "Test lead new",
            'partner_id': self.env.ref("base.res_partner_1").id,
            'description': "This is the description of the test new lead.",
            'team_id': self.env.ref("sales_team.team_sales_department").id
        })
        self.assertTrue(lead.stage_id.lead_type, 'both')

        lead.convert_opportunity(self.env.ref("base.res_partner_2").id)
        self.assertLessEqual(lead.stage_id.sequence, 1,
                             "Default stage of lead is incorrect!")
        self.assertTrue(lead.stage_id.lead_type, 'both')
        lead.action_set_won()
        self.assertTrue(lead.stage_id.lead_type, 'both')
        stage_id = lead._stage_find(domain=[('probability', '=', 100.0)])
        self.assertEqual(stage_id, lead.stage_id,
                         "Stage of opportunity is incorrect!")
        self.assertTrue(stage_id.lead_type, 'both')

    def test_crm_lead_merge(self):
        default_stage_id = self.ref("crm.stage_lead1")
        lead_salesmanager = self.env['crm.lead'].sudo(self.crm_salemanager.id)

        test_crm_opp_01 = lead_salesmanager.create({
            'type': 'opportunity',
            'name': 'Test opportunity 1',
            'partner_id': self.env.ref("base.res_partner_3").id,
            'stage_id': default_stage_id,
            'description': 'This is the description of the test opp 1.'
        })
        self.assertTrue(test_crm_opp_01.stage_id.lead_type, 'both')

        test_crm_lead_01 = lead_salesmanager.create({
            'type': 'lead',
            'name': 'Test lead first',
            'partner_id': self.env.ref("base.res_partner_1").id,
            'stage_id': default_stage_id,
            'description': 'This is the description of the test lead first.'
        })
        self.assertTrue(test_crm_lead_01.stage_id.lead_type, 'both')

        test_crm_lead_02 = lead_salesmanager.create({
            'type': 'lead',
            'name': 'Test lead second',
            'partner_id': self.env.ref("base.res_partner_1").id,
            'stage_id': default_stage_id,
            'description': 'This is the description of the test lead second.'
        })
        self.assertTrue(test_crm_lead_02.stage_id.lead_type, 'both')

        lead_ids = [
            test_crm_opp_01.id, test_crm_lead_01.id, test_crm_lead_02.id,
        ]
        add_context = {
            'active_model': 'crm.lead',
            'active_ids': lead_ids,
            'active_id': lead_ids[0],
        }

        merge_opp_wizard_01 = self.env['crm.merge.opportunity'].sudo(
            self.crm_salemanager.id).with_context(**add_context).create({})
        merge_opp_wizard_01.action_merge()

        merged_lead = self.env['crm.lead'].search([
            ('name', '=', 'Test opportunity 1'),
            ('partner_id', '=', self.env.ref("base.res_partner_3").id)],
            limit=1
        )
        self.assertTrue(merged_lead, 'Fail to create merge opportunity wizard')
        self.assertEqual(merged_lead.type, 'opportunity', 'Type mismatch')

        self.assertFalse(test_crm_lead_01.exists(),
                         'This tailing lead should not exist anymore')
        self.assertFalse(test_crm_lead_02.exists(),
                         'This tailing opp should not exist anymore')
        self.assertTrue(merged_lead.stage_id.lead_type, 'both')
