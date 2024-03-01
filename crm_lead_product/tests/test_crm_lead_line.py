# Copyright 2017-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.tests import common


class TestCrmLeadLine(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestCrmLeadLine, cls).setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.lead_line_obj = cls.env["crm.lead.line"]
        cls.lead = cls.env["crm.lead"].create(
            {
                "type": "lead",
                "name": "Test lead new",
                "partner_id": cls.env.ref("base.res_partner_1").id,
                "description": "This is the description of the test new lead.",
                "team_id": cls.env.ref("sales_team.team_sales_department").id,
            }
        )

        # Products
        cls.product_1 = cls.product_obj.create(
            {
                "name": "Product 1",
                "categ_id": cls.env.ref("product.product_category_1").id,
                "lst_price": 142.0,
            }
        )
        cls.product_2 = cls.product_obj.create(
            {
                "name": "Product 2",
                "categ_id": cls.env.ref("product.product_category_2").id,
                "lst_price": 1420.0,
            }
        )
        cls.product_3 = cls.product_obj.create(
            {
                "name": "Product 3",
                "categ_id": cls.env.ref("product.product_category_3").id,
                "lst_price": 14200.0,
            }
        )
        cls.product_4 = cls.env.ref("product.product_product_25")

    def test_01_lead_lines(self):
        """Tests for Crm Lead Line"""

        # Create new lead line with product id
        self.lead_line_1 = self.lead_line_obj.create(
            {
                "lead_id": self.lead.id,
                "name": self.product_1.name,
                "product_id": self.product_1.id,
                "uom_id": self.product_1.uom_id.id,
                "price_unit": self.product_1.lst_price,
            }
        )
        # Create new lead line with category id
        self.lead_line_2 = self.lead_line_obj.create(
            {
                "lead_id": self.lead.id,
                "name": self.product_2.categ_id.name,
                "category_id": self.product_2.categ_id.id,
            }
        )
        # Create new lead line with product template
        self.lead_line_3 = self.lead_line_obj.create(
            {
                "lead_id": self.lead.id,
                "name": self.product_3.product_tmpl_id.name,
                "product_tmpl_id": self.product_3.product_tmpl_id.id,
            }
        )

        self.lead_line_1._onchange_product_id()
        self.lead_line_2._onchange_category_id()
        self.lead_line_2._onchange_uom_id()
        self.lead_line_3._onchange_product_tmpl_id()
        self.lead_line_3._onchange_product_id()

        # Check values have been introduced correctly
        self.assertEqual(
            self.lead_line_1.category_id,
            self.product_1.categ_id,
            "Lead line category should be equal to product 1" "category",
        )
        self.assertEqual(
            self.lead_line_1.product_tmpl_id,
            self.product_1.product_tmpl_id,
            "Lead line product template should be equal to " "product 1 template",
        )
        self.assertEqual(
            self.lead_line_3.category_id,
            self.product_3.categ_id,
            "Lead line category should be equal to product 3" "category",
        )

        lead_line_4 = self.lead_line_obj.create(
            {
                "lead_id": self.lead.id,
                "name": self.product_1.name,
                "product_id": self.product_1.id,
            }
        )
        lead_line_4._onchange_product_id()

        # Change category and check that product and template are now None
        lead_line_4.write({"category_id": self.product_2.categ_id.id})
        lead_line_4._onchange_category_id()
        self.assertNotEqual(
            lead_line_4.product_id,
            self.product_1,
            "Lead line product should be equal to None",
        )
        self.assertNotEqual(
            lead_line_4.product_tmpl_id,
            self.product_1.product_tmpl_id,
            "Lead line product template should be equal " "to None",
        )

    def test_02_lead_to_opportunity(self):
        # Write one lead line to CRM Lead
        self.lead.write(
            {
                "lead_line_ids": [
                    (
                        0,
                        0,
                        {
                            "lead_id": self.lead.id,
                            "name": self.product_4.name,
                            "product_id": self.product_4.id,
                            "category_id": self.product_4.categ_id.id,
                            "price_unit": self.product_4.list_price,
                        },
                    )
                ]
            }
        )
        self.lead._onchange_lead_line_ids()

        # Check if planned revenue is correctly set for lead line 1
        self.assertEqual(
            self.lead.lead_line_ids[0].planned_revenue,
            self.product_4.list_price,
            "Planned revenue should be equal " "to the product standard price",
        )

        self.lead.convert_opportunity(self.env.ref("base.res_partner_1"))

        lead_line_1 = self.lead.lead_line_ids[0]

        self.assertEqual(
            lead_line_1.expected_revenue,
            lead_line_1.planned_revenue * self.lead.probability * (1 / 100),
            "Expected revenue should be planned " "revenue times the probability",
        )

        self.lead.write({"probability": 30})

        self.assertEqual(
            lead_line_1.expected_revenue,
            round(lead_line_1.planned_revenue * self.lead.probability * (1 / 100), 5),
            "Expected revenue should be planned " "revenue times the probability",
        )
