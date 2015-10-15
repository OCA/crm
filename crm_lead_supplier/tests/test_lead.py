# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        values = {
            "name": __file__,
            "partner_name": u"HÎ",
            "supplier": True,
        }
        self.lead = self.env["crm.lead"].create(values)
        self.partner = self.env["res.partner"].create(values)

    def test_transfered_values(self):
        """Fields get transfered when creating partner."""
        self.lead.handle_partner_assignation()
        self.assertEqual(self.lead.partner_id.supplier,
                         self.lead.supplier)

    def test_onchange_partner_id(self):
        """Lead gets supplier from partner when linked to it."""
        self.lead.supplier = False
        self.lead.partner_id = self.partner
        result = self.lead.on_change_partner_id(self.partner.id)
        self.assertEqual(result["value"]["supplier"], self.partner.supplier)
