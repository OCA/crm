# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({"name": __file__})
        self.partner = self.env["res.partner"].create({"name": __file__})
        self.test_website = "http://antiun.net"

    def test_mapped_values(self):
        """Website gets mapped when creating partner."""
        self.lead.website = self.test_website
        mapped = self.lead._map_values_to_partner(self.lead.name, False)[0]
        self.assertEqual(mapped["website"], self.test_website)

    def test_onchange_partner_id(self):
        """Lead gets website from partner when linked to it."""
        self.partner.website = self.test_website
        self.lead.partner_id = self.partner
        result = self.lead.on_change_partner_id(self.partner.id)
        self.assertEqual(result["value"]["website"], self.test_website)
