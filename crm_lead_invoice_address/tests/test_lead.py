# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "partner_name": u"HÎ",
            "invoice_equal": False,
        })
        self.partner = self.env["res.partner"].create({"name": __file__})

    def test_transfered_values(self):
        """Field gets transfered when creating partner."""
        self.lead.invoice_street = "invoice_street"
        self.lead.invoice_street2 = "invoice_street2"
        self.lead.invoice_city = "invoice_city"
        self.lead.invoice_zip = "invoice_zip"
        self.lead.invoice_state_id = self.env.ref("base.state_us_2")
        self.lead.invoice_country_id = self.env.ref("base.us")

        self.lead.handle_partner_assignation()

        self.assertEqual(
            self.lead.partner_id.type,
            "invoice")
        self.assertEqual(
            self.lead.partner_id.street,
            self.lead.invoice_street)
        self.assertEqual(
            self.lead.partner_id.street2,
            self.lead.invoice_street2)
        self.assertEqual(
            self.lead.partner_id.city,
            self.lead.invoice_city)
        self.assertEqual(
            self.lead.partner_id.zip,
            self.lead.invoice_zip)
        self.assertEqual(
            self.lead.partner_id.state_id,
            self.lead.invoice_state_id)
        self.assertEqual(
            self.lead.partner_id.country_id,
            self.lead.invoice_country_id)

    def test_state_id_change(self):
        """Country reflects state change."""
        state = self.env.ref("base.state_us_2")
        self.lead.invoice_state_id = state
        self.lead._invoice_state_id_change()

        self.assertEqual(self.lead.invoice_country_id, state.country_id)
