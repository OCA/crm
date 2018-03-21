# Copyright 2018 brain-tec AG <kumar.aberer@braintec-group.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCrmLead(TransactionCase):

    def test_lead_create_contact(self):
        industry_obj = self.env['res.partner.industry']
        industry = industry_obj.create({'name': 'Test 01'})

        lead_vals = {
            'name': 'test',
            'partner_name': 'test',
            'industry_id': industry.id,
        }
        lead = self.env['crm.lead'].create(lead_vals)
        partner_vals = lead._create_lead_partner_data(
            lead.name, True, False)
        self.assertEqual(partner_vals.get('industry_id'),
                         lead.industry_id.id)

    def test_lead_onchange_partner(self):
        industry_obj = self.env['res.partner.industry']
        industry = industry_obj.create({'name': 'Test 01'})

        partner = self.env.ref('base.partner_root')
        partner.industry_id = industry

        partner_vals = self.env['crm.lead']. \
            _onchange_partner_id_values(partner.id)

        self.assertEqual(partner.industry_id.id,
                         partner_vals.get('industry_id'))
