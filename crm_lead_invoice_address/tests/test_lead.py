# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from .. import exceptions as ex


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "partner_name": u"HÎ",
            "contact_name": u"Yoü",
            "invoice_equal": False,
        })
        self.partner = self.env["res.partner"].create({"name": __file__})
        self.fields = (
            "street",
            "street2",
            "city",
            "zip",
            "state_id",
            "country_id",
        )

    def tearDown(self):
        if self.lead.partner_id:
            self.assertEqual(self.lead.partner_id.type, "contact")
            self.assertEqual(self.lead.partner_id.parent_id.type, "invoice")

            for field in self.fields:
                self.assertEqual(
                    self.lead.partner_id[field],
                    self.lead[field],
                    "Checking field %s" % field)
                self.assertEqual(
                    self.lead.partner_id.parent_id[field],
                    self.lead["invoice_%s" % field],
                    "Checking field invoice_%s" % field)

        return super(LeadCase, self).tearDown()

    def test_no_address_mix(self):
        """Addresses do not get mixed.

        If this happens, some ``street2`` could get mixed with
        ``invoice_street`` for example.
        """
        self.lead.write({
            "street": "street",
            "street2": "street2",
            "city": "city",
            "zip": "zip",
            "state_id": self.env.ref("base.state_us_2").id,
            "country_id": self.env.ref("base.us").id,
        })
        self.lead.handle_partner_assignation()

    def test_required_contact_name(self):
        """Need :attr:`~.contact_name` for adding invoice address to one."""
        self.lead.contact_name = False
        with self.assertRaises(ex.Need2PartnersError):
            self.lead.handle_partner_assignation()

    def test_required_partner_name(self):
        """Need :attr:`~.partner_name` for adding invoice address to one."""
        self.lead.partner_name = False
        with self.assertRaises(ex.Need2PartnersError):
            self.lead.handle_partner_assignation()

    def test_transfered_values(self):
        """Field gets transfered when creating partner."""
        self.lead.invoice_street = "invoice_street"
        self.lead.invoice_street2 = "invoice_street2"
        self.lead.invoice_city = "invoice_city"
        self.lead.invoice_zip = "invoice_zip"
        self.lead.invoice_state_id = self.env.ref("base.state_us_2")
        self.lead.invoice_country_id = self.env.ref("base.us")

        self.lead.handle_partner_assignation()

    def test_state_id_change(self):
        """Country reflects state change."""
        state = self.env.ref("base.state_us_2")
        self.lead.invoice_state_id = state
        self.lead._invoice_state_id_change()

        self.assertEqual(self.lead.invoice_country_id, state.country_id)
