# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "partner_name": u"HÎ"
        })
        self.partner = self.env["res.partner"].create({"name": __file__})
        self.test_field = "https://www.tecnativa.com"

    def test_transfered_values(self):
        """Field gets transfered when creating partner."""
        self.lead.website = self.test_field
        self.lead.handle_partner_assignation()
        self.assertEqual(self.lead.partner_id.website, self.test_field)

    def test_onchange_partner_id(self):
        """Lead gets website from partner when linked to it."""
        self.partner.website = self.test_field
        self.lead.partner_id = self.partner
        result = self.lead.on_change_partner_id(self.partner.id)
        self.assertEqual(result["value"]["website"], self.test_field)
