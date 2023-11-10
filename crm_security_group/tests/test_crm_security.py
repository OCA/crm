# Copyright 2021-2023 Tecnativa - Víctor Martínez
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo.exceptions import AccessError
from odoo.tests import Form, common, new_test_user
from odoo.tests.common import users

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestCrmSecurity(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        group_crm_all_leads = "crm_security_group.group_crm_all_leads"
        group_sale_salesman_all_leads = "sales_team.group_sale_salesman_all_leads"
        new_test_user(
            cls.env,
            login="crm_user",
            groups=group_crm_all_leads,
        )
        new_test_user(
            cls.env,
            login="sale_user",
            groups=group_sale_salesman_all_leads,
        )
        new_test_user(
            cls.env,
            login="crm_sale_user",
            groups="%s,%s" % (group_crm_all_leads, group_sale_salesman_all_leads),
        )
        cls.crm_menu = cls.env.ref("crm.crm_menu_root")
        cls.sale_menu = cls.env.ref("sale.sale_menu_root")
        # Force to active sale_menu_root (similar with sale_management installed)
        cls.sale_menu.active = True
        # create items to test after
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.crm_lead = cls.env["crm.lead"].sudo().create({"name": "Lead"})
        cls.sale_order = (
            cls.env["sale.order"].sudo().create({"partner_id": cls.partner.id})
        )

    @users("crm_user")
    def test_user_crm_only(self):
        items = self.env["ir.ui.menu"]._visible_menu_ids()
        self.assertIn(self.crm_menu.id, items)
        self.assertNotIn(self.sale_menu.id, items)
        # Crm lead checks
        crm_lead = self.env["crm.lead"].browse(self.crm_lead.id)
        with self.assertRaises(AccessError):
            crm_lead.unlink()
        crm_lead_form = Form(self.env["crm.lead"])
        crm_lead_form.name = "Lead"
        crm_lead_form.save()

    @users("sale_user")
    def test_user_sale(self):
        items = self.env["ir.ui.menu"]._visible_menu_ids()
        self.assertNotIn(self.crm_menu.id, items)
        self.assertIn(self.sale_menu.id, items)
        # Crm lead checks
        crm_lead = self.env["crm.lead"].browse(self.crm_lead.id)
        with self.assertRaises(AccessError):
            crm_lead.unlink()
        crm_lead_form = Form(self.env["crm.lead"])
        crm_lead_form.name = "Lead"
        crm_lead_form.save()
        # Sale order checks
        sale_order = self.env["sale.order"].browse(self.sale_order.id)
        with self.assertRaises(AccessError):
            sale_order.unlink()
        sale_order_form = Form(self.env["sale.order"])
        sale_order_form.partner_id = self.partner
        sale_order_form.save()

    @users("crm_sale_user")
    def test_user_crm_sale(self):
        items = self.env["ir.ui.menu"]._visible_menu_ids()
        self.assertIn(self.crm_menu.id, items)
        self.assertIn(self.sale_menu.id, items)
        # Crm lead checks
        crm_lead = self.env["crm.lead"].browse(self.crm_lead.id)
        with self.assertRaises(AccessError):
            crm_lead.unlink()
        crm_lead_form = Form(self.env["crm.lead"])
        crm_lead_form.name = "Lead"
        crm_lead_form.save()
        # Sale order checks
        sale_order = self.env["sale.order"].browse(self.sale_order.id)
        with self.assertRaises(AccessError):
            sale_order.unlink()
        sale_order_form = Form(self.env["sale.order"])
        sale_order_form.partner_id = self.partner
        sale_order_form.save()
