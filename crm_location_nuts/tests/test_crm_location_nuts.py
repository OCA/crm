# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo.addons.base_location_nuts.tests.test_base_location_nuts\
    import TestBaseLocationNuts


class TestCrmNuts(TestBaseLocationNuts):
    @classmethod
    def setUpClass(cls):
        super(TestCrmNuts, cls).setUpClass()
        cls.nuts1_1 = cls.env[
            'res.partner.nuts'].search([('code', '=', 'ES')])
        cls.lead = cls.env['crm.lead'].create({
            'name': 'Test Lead',
            'contact_name': 'Mr. Odoo',
            'nuts1_id': cls.nuts1_1.id,
            'nuts2_id': cls.nuts2_1.id,
            'nuts3_id': cls.nuts3_1.id,
            'nuts4_id': cls.nuts4_1.id,
        })

    def test_create_partner(self):
        partner = self.lead._create_lead_partner()
        self.assertEqual(partner.nuts1_id, self.nuts1_1)
        self.assertEqual(partner.nuts2_id, self.nuts2_1)
        self.assertEqual(partner.nuts3_id, self.nuts3_1)
        self.assertEqual(partner.nuts4_id, self.nuts4_1)

    def test_onchange_crm_nuts_country(self):
        self.lead.nuts1_id = self.nuts1_2
        self.lead._onchange_nuts1_id()
        self.assertEqual(self.lead.country_id, self.nuts1_2.country_id)

    def test_onchange_nuts_crm(self):
        self.lead.country_id = self.country_2
        self.lead._onchange_country_id_crm_location_nuts()
        self.assertEqual(self.lead.nuts1_id.country_id,
                         self.lead.country_id)
        self.lead.nuts4_id = self.nuts4_1
        self.lead._onchange_nuts4_id()
        self.assertEqual(self.lead.country_id,
                         self.country_1)
        self.assertEqual(self.lead.nuts3_id, self.nuts3_1)
        self.lead._onchange_nuts3_id()
        self.assertEqual(self.lead.nuts2_id, self.nuts2_1)
        self.lead._onchange_nuts2_id()
        self.assertEqual(self.lead.nuts1_id.country_id, self.country_1)
        self.lead.country_id = self.country_2
        self.lead._onchange_country_id_crm_location_nuts()
        self.assertEqual(self.lead.country_id, self.nuts1_2.country_id)
        self.assertFalse(self.lead.nuts2_id)
        self.assertFalse(self.lead.nuts3_id)
        self.assertFalse(self.lead.nuts4_id)

    def test_onchange_states_crm(self):
        self.lead.state_id = self.state_2
        self.lead._onchange_state_id_crm_location_nuts()
        self.assertEqual(self.state_2, self.lead.nuts4_id.state_id)
        self.lead.state_id = self.state_1
        self.lead._onchange_state_id_crm_location_nuts()
        self.assertEqual(self.state_1, self.lead.nuts4_id.state_id)
        self.lead._onchange_nuts4_id()
        self.assertEqual(self.lead.nuts3_id, self.nuts3_1)
        self.lead._onchange_nuts3_id()
        self.assertEqual(self.lead.nuts2_id, self.nuts2_1)
        self.lead._onchange_nuts2_id()
        self.assertEqual(self.lead.nuts1_id.country_id, self.country_1)
