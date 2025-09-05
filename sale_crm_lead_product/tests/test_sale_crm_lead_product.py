# Copyright (C) 2024 ForgeFlow
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import TransactionCase


class TestSaleOrderOpportunity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env["product.product"]
        cls.Lead = cls.env["crm.lead"]
        cls.SaleOrder = cls.env["sale.order"]

        cls.product = cls.Product.create(
            {
                "name": "Test Product",
                "list_price": 100.0,
            }
        )

        cls.opportunity = cls.Lead.create(
            {
                "name": "Test Opportunity",
            }
        )
        cls.lead_line = cls.env["crm.lead.line"].create(
            {
                "lead_id": cls.opportunity.id,
                "product_id": cls.product.id,
                "name": "Test Lead Line",
                "uom_id": cls.product.uom_id.id,
                "product_qty": 2.0,
                "price_unit": 50.0,
            }
        )

        cls.sale_order = cls.SaleOrder.create(
            {
                "partner_id": cls.env.ref("base.res_partner_1").id,
                "opportunity_id": cls.opportunity.id,
            }
        )

    def test_01_compute_show_copy_products_from_opportunity(self):
        """Test compute field behavior."""

        self.sale_order._compute_show_copy_products_from_opportunity()
        self.assertTrue(self.sale_order.show_copy_products_from_opportunity)

        self.sale_order.copy_products_from_opportunity()

        # After copying, it should be False (all lead lines copied)
        self.sale_order._compute_show_copy_products_from_opportunity()
        self.assertFalse(self.sale_order.show_copy_products_from_opportunity)

    def test_02_copy_products_from_opportunity_creates_order_lines(self):
        """Test that copying lead lines creates correct sale order lines."""
        self.sale_order.copy_products_from_opportunity()
        self.assertEqual(len(self.sale_order.order_line), 1)
        line = self.sale_order.order_line[0]
        self.assertEqual(line.product_id, self.product)
        self.assertEqual(line.product_uom_qty, 2.0)
        self.assertEqual(line.price_unit, 50.0)
        self.assertEqual(line.crm_lead_line_id, self.lead_line)
