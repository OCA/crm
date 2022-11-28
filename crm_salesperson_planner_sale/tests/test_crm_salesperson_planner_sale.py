# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests import Form

from odoo.addons.crm_salesperson_planner.tests.test_crm_salesperson_planner_visit import (
    TestCrmSalespersonPlannerVisitBase,
)


class TestCrmSalespersonPlannerSale(TestCrmSalespersonPlannerVisitBase):
    def _create_sale_order_from_visit(self, visit):
        res = self.visit1.action_sale_quotation_new()
        order_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        return order_form.save()

    def test_visit_process(self):
        self.assertFalse(self.visit1.order_ids)
        order = self._create_sale_order_from_visit(self.visit1)
        self.assertEqual(order.visit_id, self.visit1)
        self.assertIn(order, self.visit1.order_ids)
        self.assertEqual(self.visit1.sale_order_count, 0)
        self.assertEqual(self.visit1.quotation_count, 1)
        res = self.visit1.action_view_sale_quotation()
        self.assertIn(order, self.env[res["res_model"]].search(res["domain"]))
        self.assertEqual(res["res_id"], order.id)
        order.write({"state": "sale"})
        self.assertEqual(self.visit1.sale_order_count, 1)
        self.assertEqual(self.visit1.quotation_count, 0)
        res = self.visit1.action_view_sale_order()
        self.assertIn(order, self.env[res["res_model"]].search(res["domain"]))
        self.assertEqual(res["res_id"], order.id)
