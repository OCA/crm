# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "invoice_equal": False,
        })
        self.partner = self.env["res.partner"].create({"name": __file__})

    def test_mapped_values(self):
        """Invoice address gets mapped when creating partner."""
        self.lead.invoice_street = "invoice_street"
        self.lead.invoice_street2 = "invoice_street2"
        self.lead.invoice_city = "invoice_city"
        self.lead.invoice_zip = "invoice_zip"
        self.lead.invoice_state_id = self.env.ref("base.state_us_2")
        self.lead.invoice_country_id = self.env.ref("base.us")

        mapped = self.lead._map_values_to_partner(self.lead.name, True)[0]

        self.assertEqual(mapped["type"], "invoice")
        self.assertEqual(mapped["street"], self.lead.invoice_street)
        self.assertEqual(mapped["street2"], self.lead.invoice_street2)
        self.assertEqual(mapped["city"], self.lead.invoice_city)
        self.assertEqual(mapped["zip"], self.lead.invoice_zip)
        self.assertEqual(mapped["state_id"], self.lead.invoice_state_id.id)
        self.assertEqual(mapped["country_id"], self.lead.invoice_country_id.id)

    def test_state_id_change(self):
        """Country reflects state change."""
        state = self.env.ref("base.state_us_2")
        self.lead.invoice_state_id = state
        self.lead._invoice_state_id_change()

        self.assertEqual(self.lead.invoice_country_id, state.country_id)
