# Copyright 2022 Telmo Santos <telmo.santos@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    request_type = fields.Selection(
        [
            ("customer", "Customer Lead"),
            ("supplier", "Supplier Lead"),
        ],
    )
    purchase_amount_total = fields.Monetary(
        compute="_compute_purchase_data",
        string="Sum of Orders",
        help="Untaxed Total of Confirmed Orders",
        currency_field="company_currency",
    )
    request_for_quotation_count = fields.Integer(
        compute="_compute_purchase_data", string="Number of Quotations"
    )
    purchase_order_count = fields.Integer(
        compute="_compute_purchase_data", string="Number of Purchase Orders"
    )
    purchase_order_ids = fields.One2many(
        "purchase.order", "opportunity_id", string="Purchase Orders"
    )

    @api.depends(
        "order_ids.state",
        "order_ids.currency_id",
        "order_ids.amount_untaxed",
        "order_ids.date_order",
        "order_ids.company_id",
    )
    def _compute_purchase_data(self):
        for lead in self:
            total = 0.0
            rfq_cnt = 0
            purchase_order_cnt = 0
            company_currency = lead.company_currency or self.env.company.currency_id
            for order in lead.purchase_order_ids:
                if order.state in ("draft", "sent"):
                    rfq_cnt += 1
                if order.state not in ("draft", "sent", "cancel"):
                    purchase_order_cnt += 1
                    total += order.currency_id._convert(
                        order.amount_untaxed,
                        company_currency,
                        order.company_id,
                        order.date_order or fields.Date.today(),
                    )
            lead.purchase_amount_total = total
            lead.request_for_quotation_count = rfq_cnt
            lead.purchase_order_count = purchase_order_cnt

    def _create_customer(self):
        """It can be a customer or supplier depending on lead request type"""
        self = self.with_context(res_partner_search_mode=self.request_type)
        return super(CrmLead, self)._create_customer()

    def action_lead_rfq_new(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id(
                "srm.srm_rfq_partner_action"
            )
        else:
            return self.action_rfq_new()

    def action_rfq_new(self):
        action = self.env["ir.actions.actions"]._for_xml_id("srm.action_lead_rfq_new")
        action["context"] = {
            "default_partner_id": self.partner_id.id,
            "default_opportunity_id": self.id,
        }
        if self.user_id:
            action["context"]["default_user_id"] = self.user_id.id
        return action
