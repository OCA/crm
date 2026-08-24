# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import defaultdict

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    user_id = fields.Many2one(string="Responsible")
    team_id = fields.Many2one(string="Team")

    request_type = fields.Selection(
        selection=[
            ("customer", "Customer Lead"),
            ("supplier", "Supplier Lead"),
        ],
    )
    purchase_amount_total = fields.Monetary(
        compute="_compute_purchase_amount_total",
        string="Sum of Purchase Orders",
        help="Untaxed Total of Confirmed Purchase Orders",
        currency_field="company_currency",
    )
    request_for_quotation_count = fields.Integer(
        compute="_compute_request_for_quotation_count",
        string="Number of Request for Quotations",
    )
    purchase_order_count = fields.Integer(
        compute="_compute_purchase_order_count", string="Number of Purchase Orders"
    )
    purchase_order_ids = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="opportunity_id",
        string="Purchase Orders",
    )

    def _get_lead_purchase_order_domain(self):
        return [("state", "not in", ("draft", "sent", "cancel"))]

    def _get_lead_request_for_quotation_domain(self):
        return [("state", "in", ("draft", "sent"))]

    @api.depends("purchase_order_ids.state")
    def _compute_purchase_order_count(self):
        purchase_order_per_lead = {
            lead.id: count
            for lead, count in self.env["purchase.order"]._read_group(
                domain=[
                    ("opportunity_id", "in", self.ids),
                    *self._get_lead_purchase_order_domain(),
                ],
                groupby=["opportunity_id"],
                aggregates=["__count"],
            )
        }
        for lead in self:
            lead.purchase_order_count = purchase_order_per_lead.get(lead.id, 0)

    @api.depends("purchase_order_ids.state")
    def _compute_request_for_quotation_count(self):
        rfq_per_lead = {
            lead.id: count
            for lead, count in self.env["purchase.order"]._read_group(
                domain=[
                    ("opportunity_id", "in", self.ids),
                    *self._get_lead_request_for_quotation_domain(),
                ],
                groupby=["opportunity_id"],
                aggregates=["__count"],
            )
        }
        for lead in self:
            lead.request_for_quotation_count = rfq_per_lead.get(lead.id, 0)

    @api.depends(
        "purchase_order_ids.state",
        "purchase_order_ids.currency_id",
        "purchase_order_ids.amount_untaxed",
        "purchase_order_ids.date_order",
        "purchase_order_ids.company_id",
    )
    def _compute_purchase_amount_total(self):
        amount_per_lead = defaultdict(float)

        for (
            lead,
            currency,
            company,
            date_order,
            amount,
        ) in self.env["purchase.order"]._read_group(
            domain=[
                ("opportunity_id", "in", self.ids),
                *self._get_lead_purchase_order_domain(),
            ],
            groupby=["opportunity_id", "currency_id", "company_id", "date_order:day"],
            aggregates=["amount_untaxed:sum"],
        ):
            company_currency = lead.company_currency or self.env.company.currency_id
            amount_per_lead[lead.id] += currency._convert(
                amount,
                company_currency,
                company,
                date_order or fields.Date.context_today(self),
            )

        for lead in self:
            lead.purchase_amount_total = amount_per_lead.get(lead.id, 0.0)

    def _create_customer(self):
        """It can be a customer or supplier depending on lead request type"""
        self = self.with_context(res_partner_search_mode=self.request_type)
        return super()._create_customer()

    def action_lead_rfq_new(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id(
                "srm.srm_rfq_partner_action"
            )
        else:
            return self.action_rfq_new()

    def action_rfq_new(self):
        action = self.env["ir.actions.actions"]._for_xml_id("srm.action_lead_rfq_new")
        action["context"] = self._prepare_rfq_context()
        return action

    def _prepare_rfq_context(self):
        self.ensure_one()
        rfq_context = {
            "default_partner_id": self.partner_id.id,
            "default_opportunity_id": self.id,
        }
        if self.user_id:
            rfq_context["default_user_id"] = self.user_id.id
        return rfq_context
