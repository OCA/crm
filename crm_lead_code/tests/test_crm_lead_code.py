##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from odoo.tests.common import TransactionCase


class TestCrmLeadCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.crm_lead_model = cls.env["crm.lead"]
        cls.ir_sequence_model = cls.env["ir.sequence"]
        cls.crm_sequence = cls.env.ref("crm_lead_code.sequence_lead")
        cls.crm_lead = cls.env.ref("crm.crm_case_1")

    def test_old_lead_code_assign(self):
        crm_leads = self.crm_lead_model.search([])
        for crm_lead in crm_leads:
            self.assertNotEqual(crm_lead.code, "/")

    def test_new_lead_code_assign(self):
        code = self._get_next_code()
        crm_lead = self.crm_lead_model.create({"name": "Testing lead code"})
        self.assertNotEqual(crm_lead.code, "/")
        self.assertEqual(crm_lead.code, code)

    def test_copy_lead_code_assign(self):
        code = self._get_next_code()
        crm_lead_copy = self.crm_lead.copy()
        self.assertNotEqual(crm_lead_copy.code, self.crm_lead.code)
        self.assertEqual(crm_lead_copy.code, code)

    def _get_next_code(self):
        return self.crm_sequence.get_next_char(self.crm_sequence.number_next_actual)
