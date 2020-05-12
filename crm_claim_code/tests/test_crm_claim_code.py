# Copyright 2015 Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 AvanzOsc (http://www.avanzosc.es)
# Copyright 2017 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestCrmClaimCode(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCrmClaimCode, cls).setUpClass()
        cls.crm_claim_model = cls.env['crm.claim']
        cls.ir_sequence_model = cls.env['ir.sequence']
        cls.crm_sequence = cls.env.ref('crm_claim_code.sequence_claim')
        cls.crm_claim = cls.env['crm.claim'].create({
            'name': 'Test Claim',
        })

    def test_old_claim_code_assign(self):
        crm_claims = self.crm_claim_model.search([])
        for crm_claim in crm_claims:
            self.assertNotEqual(crm_claim.code, '/')

    def test_new_claim_code_assign(self):
        code = self._get_next_code()
        crm_claim = self.crm_claim_model.create({
            'name': 'Testing claim code',
        })
        self.assertNotEqual(crm_claim.code, '/')
        self.assertEqual(crm_claim.code, code)

    def test_copy_claim_code_assign(self):
        code = self._get_next_code()
        crm_claim_copy = self.crm_claim.copy()
        self.assertNotEqual(crm_claim_copy.code, self.crm_claim.code)
        self.assertEqual(crm_claim_copy.code, code)

    def _get_next_code(self):
        return self.crm_sequence.get_next_char(
            self.crm_sequence.number_next_actual
        )
