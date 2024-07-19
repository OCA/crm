# Copyright 2017 Tecnativa - Luis M. Ontalba
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0

from odoo.addons.base.tests.common import BaseCommon


class TestCrmLocation(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env["res.country"].create(
            {"name": "Test country", "code": "AA"}
        )
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

    def test_compute_partner_address_values(self):
        self.lead.location_id = self.location.id
        self.lead._compute_partner_address_values()
        self.assertEqual(self.lead.zip, "12345")
        self.assertEqual(self.lead.city, "Test city")
        self.assertEqual(self.lead.state_id.name, "Test state")
        self.assertEqual(self.lead.country_id.name, "Test country")

    def test_compute_location_id(self):
        self.partner.zip_id = self.location.id
        self.lead.partner_id = self.partner.id
        self.lead._compute_location_id()
        self.assertEqual(self.lead.location_id.name, "12345")
