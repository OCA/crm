# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.medium = cls.env["utm.medium"].create({"name": "Website"})
        cls.campaign = cls.env["utm.campaign"].create({"name": "Dëmo campaign"})
        cls.source = cls.env["utm.source"].create({"name": "Inteŕnet"})
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Lead1",
                "medium_id": cls.medium.id,
                "campaign_id": cls.campaign.id,
                "source_id": cls.source.id,
            }
        )

    def test_transfered_values(self):
        """Fields get transfered when creating partner."""
        self.lead._handle_partner_assignment()
        if self.lead.partner_id:
            for _key, field, _cookie in self.env["utm.mixin"].tracking_fields():
                self.assertEqual(self.lead[field], self.lead.partner_id[field])
                self.assertIsNot(False, self.lead.partner_id[field])
