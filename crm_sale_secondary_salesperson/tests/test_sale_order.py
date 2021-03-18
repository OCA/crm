# Copyright 2021 Tecnativa - Víctor Martínez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo.tests import Form, common


class TestSaleOrder(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.user_demo = cls.env.ref("base.user_demo")
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": cls.partner.id,
                "user_id": cls.user_admin.id,
                "secondary_user_id": cls.user_demo.id,
            }
        )

    def test_sale_order_with_opportunity_id(self):
        order = Form(self.env["sale.order"])
        order.partner_id = self.partner
        order.opportunity_id = self.lead
        order.save()
        self.assertEqual(order.secondary_user_id, self.lead.secondary_user_id)
