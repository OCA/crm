# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "partner_name": u"HÎ"
        })

    def _fulfill(self, record):
        """Fulfill a record's marketing fields with some data."""
        record.write({
            "medium_id": self.env['utm.medium'].create({
                'name': u'Medíum Website'
            }).id,
            "campaign_id": self.env["utm.campaign"].create({
                "name": u"Dëmo campaign",
            }).id,
            "source_id": self.env['utm.source'].create({
                'name': u'Inteŕnet'
            }).id,
        })

    def test_transfered_values(self):
        """Fields get transfered when creating partner."""
        self._fulfill(self.lead)
        self.lead.handle_partner_assignation()
        for _key, field, cookie in self.lead.tracking_fields():
            self.assertEqual(self.lead[field], self.lead.partner_id[field])
            self.assertIsNot(False, self.lead.partner_id[field])
