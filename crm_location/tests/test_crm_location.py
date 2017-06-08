# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0

from odoo.tests import common


class TestCrmLocation(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCrmLocation, cls).setUpClass()
        cls.country = cls.env['res.country'].create({
            'name': 'Country test',
        })
        cls.state = cls.env['res.country.state'].create({
            'name': 'Test state',
            'code': 'Test state code',
            'country_id': cls.country.id,
        })
        cls.location = cls.env['res.better.zip'].create({
            'name': '12345',
            'city': 'Test city',
            'country_id': cls.country.id,
            'code': 'Test code',
            'state_id': cls.state.id,
        })
        cls.lead = cls.env['crm.lead'].create({
            'name': 'Test lead',
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner name',
        })

    def test_on_change_city(self):
        lead = self.lead
        location = self.location
        lead.location_id = location.id
        lead.on_change_city()
        self.assertEqual(lead.zip, location.name)
        self.assertEqual(lead.city, location.city)
        self.assertEqual(lead.state_id, location.state_id)
        self.assertEqual(lead.country_id, location.country_id)

    def test_onchange_partner_id_crm_location(self):
        lead = self.lead
        partner = self.partner
        location = self.location
        partner.zip_id = location.id
        lead.partner_id = partner.id
        lead.onchange_partner_id_crm_location()
        self.assertEqual(lead.location_id, partner.zip_id)
