# Copyright 2020 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({
            "name": "My test partner",
        })
        self.tag = self.env["crm.lead.tag"].create({
            "name": "My tag",
        })
        self.lead = self.env["crm.lead"].create({
            "name": "My lead",
            "partner_id": self.partner.id,
            "tag_ids": [(4, self.tag.id)],
        })
        self.sale_order = self.env["sale.order"].create({
            "opportunity_id": self.lead.id,
            "partner_id": self.partner.id,
            "tag_ids": [(4, self.tag.id)],
        })

    def test_sync_on_lead(self):
        """ Sale order tags are synchronized when editing lead tags """
        tag = self.env["crm.lead.tag"].create({"name": "Lead Tag"})
        self.lead.tag_ids = tag
        self.assertEqual(self.sale_order.tag_ids, tag)

    def test_sync_on_sale_order(self):
        """ Lead tags are synchronized when editing sale order tags """
        tag = self.env["crm.lead.tag"].create({"name": "Sale Order Tag"})
        self.sale_order.tag_ids = tag
        self.assertEqual(self.lead.tag_ids, tag)

    def test_sync_on_lead_change(self):
        """ Sale order tags are taken from new lead, if a new one is set """
        tags = self.env["crm.lead.tag"].search([])
        lead = self.env["crm.lead"].create({
            "name": "New lead",
            "partner_id": self.partner.id,
            "tag_ids": [(4, tag_id) for tag_id in tags.ids],
        })
        self.sale_order.opportunity_id = lead.id
        self.assertEqual(self.sale_order.tag_ids, tags)

    def test_sale_without_lead(self):
        """ Sale order without opportunity shouldn't synchronize anything """
        tags = self.sale_order.tag_ids
        opportunity = self.sale_order.opportunity_id
        self.sale_order.opportunity_id = False
        self.assertEqual(self.sale_order.tag_ids, tags)
        self.sale_order.tag_ids = [(5)]
        self.assertEqual(opportunity.tag_ids, tags)
