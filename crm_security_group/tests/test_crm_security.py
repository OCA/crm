# Copyright 2021 Tecnativa - Víctor Martínez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo.exceptions import AccessError
from odoo.tests.common import Form, SavepointCase


class TestCrmSecurity(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_user = cls.env.ref("base.group_user")
        cls.group_crm_all_leads = cls.env.ref("crm_security_group.group_crm_all_leads")
        cls.group_sale_salesman_all_leads = cls.env.ref(
            "sales_team.group_sale_salesman_all_leads"
        )
        cls.crm_user = cls.env["res.users"].create(
            {
                "name": "crm_user",
                "login": "crm_user",
                "email": "example@crm_user.com",
                "groups_id": [(6, 0, [cls.group_user.id, cls.group_crm_all_leads.id])],
            }
        )
        cls.sale_user = cls.env["res.users"].create(
            {
                "name": "sale_user",
                "login": "sale_user",
                "email": "example@sale_user.com",
                "groups_id": [
                    (6, 0, [cls.group_user.id, cls.group_sale_salesman_all_leads.id])
                ],
            }
        )
        cls.crm_sale_user = cls.env["res.users"].create(
            {
                "name": "crm_sale_user",
                "login": "crm_sale_user",
                "email": "example@crm_sale_user.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            cls.group_user.id,
                            cls.group_crm_all_leads.id,
                            cls.group_sale_salesman_all_leads.id,
                        ],
                    )
                ],
            }
        )
        cls.model_ir_ui_menu = cls.env["ir.ui.menu"]
        cls.crm_menu = cls.env.ref("crm.crm_menu_root")
        cls.sale_menu = cls.env.ref("sale.sale_menu_root")
        # create items to test after
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.crm_lead = cls.env["crm.lead"].sudo().create({"name": "Lead"})
        cls.sale_order = (
            cls.env["sale.order"].sudo().create({"partner_id": cls.partner.id})
        )

    def test_user_crm_only(self):
        model = self.model_ir_ui_menu.with_user(self.crm_user)
        items = model._visible_menu_ids()
        self.assertTrue(self.crm_menu.id in items)
        self.assertFalse(self.sale_menu.id in items)
        # Crm lead checks
        crm_lead_model = self.env["crm.lead"].with_user(self.crm_user)
        crm_lead = crm_lead_model.browse(self.crm_lead.id)
        self.assertEqual(crm_lead, self.crm_lead)
        with self.assertRaises(AccessError):
            self.crm_lead.with_user(self.crm_user).unlink()
        crm_lead_form = Form(crm_lead_model)
        crm_lead_form.name = "Lead"
        crm_lead_form.save()

    def test_user_sale(self):
        model = self.model_ir_ui_menu.with_user(self.sale_user)
        items = model._visible_menu_ids()
        self.assertTrue(self.crm_menu.id in items)
        self.assertTrue(self.sale_menu.id in items)
        # Crm lead checks
        crm_lead_model = self.env["crm.lead"].with_user(self.sale_user)
        crm_lead = crm_lead_model.browse(self.crm_lead.id)
        self.assertEqual(crm_lead, self.crm_lead)
        with self.assertRaises(AccessError):
            self.crm_lead.with_user(self.sale_user).unlink()
        crm_lead_form = Form(crm_lead_model)
        crm_lead_form.name = "Lead"
        crm_lead_form.save()
        # Sale order checks
        sale_order_model = self.env["sale.order"].with_user(self.sale_user)
        sale_order = sale_order_model.browse(self.sale_order.id)
        self.assertEqual(sale_order, self.sale_order)
        with self.assertRaises(AccessError):
            self.sale_order.with_user(self.sale_user).unlink()
        sale_order_form = Form(sale_order_model)
        sale_order_form.partner_id = self.partner
        sale_order_form.save()

    def test_user_crm_sale(self):
        model = self.model_ir_ui_menu.with_user(self.crm_sale_user)
        items = model._visible_menu_ids()
        self.assertTrue(self.crm_menu.id in items)
        self.assertTrue(self.sale_menu.id in items)
        # Crm lead checks
        crm_lead_model = self.env["crm.lead"].with_user(self.crm_sale_user)
        crm_lead = crm_lead_model.browse(self.crm_lead.id)
        self.assertEqual(crm_lead, self.crm_lead)
        with self.assertRaises(AccessError):
            self.crm_lead.with_user(self.crm_sale_user).unlink()
        crm_lead_form = Form(crm_lead_model)
        crm_lead_form.name = "Lead"
        crm_lead_form.save()
        # Sale order checks
        sale_order_model = self.env["sale.order"].with_user(self.crm_sale_user)
        sale_order = sale_order_model.browse(self.sale_order.id)
        self.assertEqual(sale_order, self.sale_order)
        with self.assertRaises(AccessError):
            self.sale_order.with_user(self.crm_sale_user).unlink()
        sale_order_form = Form(sale_order_model)
        sale_order_form.partner_id = self.partner
        sale_order_form.save()
