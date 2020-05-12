# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.medium = self.env["utm.medium"].create({"name": u"Website"})
        self.campaign = self.env["utm.campaign"].create({"name": u"Dëmo campaign"})
        self.source = self.env["utm.source"].create({"name": u"Inteŕnet"})
        self.lead = self.env["crm.lead"].create(
            {
                "name": "Lead1",
                "medium_id": self.medium.id,
                "campaign_id": self.campaign.id,
                "source_id": self.source.id,
            }
        )

    def test_transfered_values(self):
        """Fields get transfered when creating partner."""
        self.lead.handle_partner_assignation()
        partner_ids = self.lead.handle_partner_assignation()
        for lead_id in partner_ids:
            self.env["crm.lead"].browse(lead_id).partner_id = partner_ids[lead_id]
        for _key, field, _cookie in self.env["utm.mixin"].tracking_fields():
            self.assertEqual(self.lead[field], self.lead.partner_id[field])
            self.assertIsNot(False, self.lead.partner_id[field])
