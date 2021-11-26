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

    def action_sale_quotation_new(self):
        action = self.env.ref(
            "crm_salesperson_planner_sale.crm_salesperson_visit_action_quotation_new"
        ).read()[0]
        action["context"] = {
            "search_default_visit_id": self.id,
            "default_visit_id": self.id,
            "search_default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_origin": self.name,
            "default_company_id": self.company_id.id or self.env.company.id,
            "default_user_id": self.user_id.id,
        }
        return action

    def action_view_sale_quotation(self):
        action = self.env.ref("sale.action_quotations_with_onboarding").read()[0]
        action["context"] = {
            "search_default_draft": 1,
            "search_default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_user_id": self.user_id.id,
            "default_origin": self.name,
            "default_company_id": self.company_id.id or self.env.company.id,
            "default_visit_id": self.id,
        }
        action["domain"] = [
            ("visit_id", "=", self.id),
            ("state", "in", ["draft", "sent"]),
        ]
        quotations = self.mapped("order_ids").filtered(
            lambda l: l.state in ("draft", "sent")
        )
        if len(quotations) == 1:
            action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
            action["res_id"] = quotations.id
        return action

    def action_view_sale_order(self):
        action = self.env.ref("sale.action_orders").read()[0]
        action["context"] = {
            "search_default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_partner_id": self.partner_id.commercial_partner_id.id,
            "default_user_id": self.user_id.id,
            "default_origin": self.name,
            "default_company_id": self.company_id.id or self.env.company.id,
            "default_visit_id": self.id,
        }
        action["domain"] = [
            ("visit_id", "=", self.id),
            ("state", "not in", ("draft", "sent", "cancel")),
        ]
        orders = self.mapped("order_ids").filtered(
            lambda l: l.state not in ("draft", "sent", "cancel")
        )
        if len(orders) == 1:
            action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
            action["res_id"] = orders.id
        return action
