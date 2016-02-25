# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


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
            "medium_id": self.env.ref("crm.crm_medium_website").id,
            "campaign_id": self.env["crm.tracking.campaign"].create({
                "name": u"Dëmo campaign",
            }).id,
            "source_id": self.env.ref("crm.crm_source_search_engine").id,
        })

    def test_transfered_values(self):
        """Fields get transfered when creating partner."""
        self._fulfill(self.lead)
        self.lead.handle_partner_assignation()
        for _key, field in self.lead.tracking_fields():
            self.assertEqual(self.lead[field], self.lead.partner_id[field])
            self.assertIsNot(False, self.lead.partner_id[field])
