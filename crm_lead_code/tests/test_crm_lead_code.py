# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

import openerp.tests.common as common


class TestCrmLeadCode(common.TransactionCase):

    def setUp(self):
        super(TestCrmLeadCode, self).setUp()
        self.crm_lead_model = self.env['crm.lead']
        self.ir_sequence_model = self.env['ir.sequence']
        self.crm_sequence = self.env.ref('crm_lead_code.sequence_lead')
        self.crm_lead = self.env.ref('crm.crm_case_1')

    def test_old_lead_code_assign(self):
        crm_leads = self.crm_lead_model.search([])
        for crm_lead in crm_leads:
            self.assertNotEqual(crm_lead.code, '/')

    def test_new_lead_code_assign(self):
        code = self._get_next_code()
        crm_lead = self.crm_lead_model.create({
            'name': 'Testing lead code',
        })
        self.assertNotEqual(crm_lead.code, '/')
        self.assertEqual(crm_lead.code, code)

    def test_copy_lead_code_assign(self):
        code = self._get_next_code()
        crm_lead_copy = self.crm_lead.copy()
        self.assertNotEqual(crm_lead_copy.code, self.crm_lead.code)
        self.assertEqual(crm_lead_copy.code, code)

    def _get_next_code(self):
        d = self.ir_sequence_model._interpolation_dict()
        prefix = self.ir_sequence_model._interpolate(
            self.crm_sequence.prefix, d)
        suffix = self.ir_sequence_model._interpolate(
            self.crm_sequence.suffix, d)
        code = (prefix + ('%%0%sd' % self.crm_sequence.padding %
                          self.crm_sequence.number_next_actual) + suffix)
        return code
