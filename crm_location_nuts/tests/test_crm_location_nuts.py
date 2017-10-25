# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo.addons.base_location_nuts.tests.test_base_location_nuts\
    import TestBaseLocationNuts


class TestCrmNuts(TestBaseLocationNuts):
    @classmethod
    def setUpClass(cls):
        super(TestCrmNuts, cls).setUpClass()
        cls.lead = cls.env['crm.lead'].create({
            'name': 'Test Lead',
            'contact_name': 'Mr. Odoo',
            'region': cls.nuts2_1.id,
            'substate': cls.nuts3_1.id,
        })

    def test_create_partner(self):
        partner = self.lead._create_lead_partner()
        self.assertEqual(partner.nuts2_id, self.nuts2_1)
        self.assertEqual(partner.nuts3_id, self.nuts3_1)
