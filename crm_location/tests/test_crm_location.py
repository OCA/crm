# Copyright 2017 Tecnativa - Luis M. Ontalba
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0

from odoo.tests import common


class TestCrmLocation(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCrmLocation, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.country = cls.env["res.country"].create({"name": "Test country"})
        cls.state = cls.env["res.country.state"].create(
            {
                "name": "Test state",
                "code": "Test state code",
                "country_id": cls.country.id,
            }
        )
        cls.city = cls.env["res.city"].create(
            {
                "name": "Test city",
                "country_id": cls.country.id,
                "state_id": cls.state.id,
            }
        )
        cls.location = cls.env["res.city.zip"].create(
            {"name": "12345", "city_id": cls.city.id}
        )
        cls.lead = cls.env["crm.lead"].create({"name": "Test lead"})
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner name",
                "state_id": cls.state.id,
                "country_id": cls.country.id,
                "city_id": cls.city.id,
            }
        )

    def test_on_change_city(self):
        self.lead.location_id = self.location.id
        self.lead.on_change_city()
        self.assertEqual(self.lead.zip, "12345")
        self.assertEqual(self.lead.city, "Test city")
        self.assertEqual(self.lead.state_id.name, "Test state")
        self.assertEqual(self.lead.country_id.name, "Test country")

    def test_onchange_partner_id_crm_location(self):
        self.partner.zip_id = self.location.id
        self.lead.partner_id = self.partner.id
        self.lead.onchange_partner_id_crm_location()
        self.assertEqual(self.lead.location_id.name, "12345")
