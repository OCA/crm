# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from lxml import etree


@common.at_install(False)
@common.post_install(True)
class TestCrmClaimRefSmartButton(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimRefSmartButton, self).setUp()
        self.post_install = True
        self.partner_1 = self.env.ref('base.res_partner_1')
        self.new_partner = self.env['res.partner'].create(
            {'name': 'Test partner for crm_claim_ref_smartbutton'}
        )
        self.claim = self.env['crm.claim'].create(
            {'name': 'Test claim for partner 1',
             'ref': 'res.partner,%s' % self.partner_1.id}
        )

    def test_count_claims(self):
        # Test a record that has a linked claim
        self.assertEqual(
            self.partner_1.crm_claim_linked_count_tech, 1,
            'Number of linked claims for partner 1 is not correct')
        # Test a record that has no linked claims
        self.assertEqual(
            self.new_partner.crm_claim_linked_count_tech, 0,
            'Number of linked claims for new partner is not correct')

    def test_fields_view_get(self):
        # Test the smart-button existence for a possible linked model
        model_name = self.env['res.request.link'].search([])[0].object
        res = self.env[model_name].fields_view_get()
        eview = etree.fromstring(res['arch'])
        xml_field = eview.xpath("//field[@name='crm_claim_linked_count_tech']")
        self.assertTrue(
            xml_field, "Smart-button not added to %s view" % model_name)
        # Test the smart-button existence for a model not linked
        for model in self.env['ir.model'].search([]):
            if not self.env['res.request.link'].search(
                    [('object', '=', model.model)]):
                model_name = model.model
                break
        res = self.env[model_name].fields_view_get()
        eview = etree.fromstring(res['arch'])
        xml_field = eview.xpath("//field[@name='crm_claim_linked_count_tech']")
        self.assertFalse(
            xml_field,
            "Smart-button incorrectly added to %s view" % model_name)
