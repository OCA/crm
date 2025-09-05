# Copyright (C) 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_copy_products_from_opportunity = fields.Boolean(
        compute="_compute_show_copy_products_from_opportunity"
    )

    @api.depends("opportunity_id", "order_line")
    def _compute_show_copy_products_from_opportunity(self):
        for rec in self:
            rec.show_copy_products_from_opportunity = False
            if rec.opportunity_id:
                rec.show_copy_products_from_opportunity = True
            lead_lines = rec.opportunity_id.lead_line_ids
            copied_lines = rec.order_line.mapped("crm_lead_line_id")
            if (
                all(lead_line in copied_lines for lead_line in lead_lines)
                or not lead_lines
            ):
                rec.show_copy_products_from_opportunity = False

    def _prepare_sale_order_line_from_lead_line(self, lead_line):
        self.ensure_one()
        return {
            "order_id": self.id,
            "product_id": lead_line.product_id.id,
            "name": lead_line.name,
            "product_uom": lead_line.uom_id.id,
            "product_uom_qty": lead_line.product_qty,
            "price_unit": lead_line.price_unit,
            "crm_lead_line_id": lead_line.id,
        }

    def copy_products_from_opportunity(self):
        self.ensure_one()
        if not self.opportunity_id:
            return
        lead_lines = self.opportunity_id.lead_line_ids
        for lead_line in lead_lines:
            self.order_line.create(
                self._prepare_sale_order_line_from_lead_line(lead_line)
            )
