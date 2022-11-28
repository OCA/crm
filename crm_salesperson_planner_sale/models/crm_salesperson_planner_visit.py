# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class CrmSalespersonPlannerVisit(models.Model):
    _inherit = "crm.salesperson.planner.visit"

    order_ids = fields.One2many("sale.order", "visit_id", string="Orders")
    sale_order_count = fields.Integer(
        compute="_compute_sale_data", string="Number of Sale Orders", store=True
    )
    quotation_count = fields.Integer(
        compute="_compute_sale_data", string="Number of Quotations", store=True
    )

    @api.depends("order_ids.state")
    def _compute_sale_data(self):
        quotation_domain = [
            ("visit_id", "in", self.ids),
            ("state", "in", ("draft", "sent")),
        ]
        quotation_data = self.env["sale.order"].read_group(
            domain=quotation_domain, fields=["visit_id"], groupby=["visit_id"]
        )
        sale_domain = [
            ("visit_id", "in", self.ids),
            ("state", "not in", ("draft", "sent", "cancel")),
        ]
        sale_data = self.env["sale.order"].read_group(
            domain=sale_domain, fields=["visit_id"], groupby=["visit_id"]
        )
        mapped_quotation_data = {
            m["visit_id"][0]: m["visit_id_count"] for m in quotation_data
        }
        mapped_sale_data = {m["visit_id"][0]: m["visit_id_count"] for m in sale_data}
        for sel in self:
            sel.quotation_count = mapped_quotation_data.get(sel.id, 0)
            sel.sale_order_count = mapped_sale_data.get(sel.id, 0)

    def _prepare_context_from_action(self):
        return {
            "search_default_visit_id": self.id,
            "default_visit_id": self.id,
            "search_default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_origin": self.name,
            "default_company_id": self.company_id.id or self.env.company.id,
            "default_user_id": self.user_id.id,
        }

    def action_sale_quotation_new(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "crm_salesperson_planner_sale.crm_salesperson_visit_action_quotation_new"
        )
        action["context"] = self._prepare_context_from_action()
        return action

    def action_view_sale_quotation(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sale.action_quotations_with_onboarding"
        )
        ctx = self._prepare_context_from_action()
        ctx.update(search_default_draft=1)
        action["context"] = ctx
        action["domain"] = [
            ("visit_id", "=", self.id),
            ("state", "in", ("draft", "sent")),
        ]
        if self.quotation_count == 1:
            action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
            quotation = self.order_ids.filtered(lambda l: l.state in ("draft", "sent"))
            action["res_id"] = quotation.id
        return action

    def action_view_sale_order(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("sale.action_orders")
        action["context"] = self._prepare_context_from_action()
        action["domain"] = [
            ("visit_id", "=", self.id),
            ("state", "not in", ("draft", "sent", "cancel")),
        ]
        if self.sale_order_count == 1:
            action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
            order = self.order_ids.filtered(
                lambda l: l.state not in ("draft", "sent", "cancel")
            )
            action["res_id"] = order.id
        return action
