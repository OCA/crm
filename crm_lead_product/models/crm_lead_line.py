# Copyright (C) 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class CrmLeadLine(models.Model):
    _name = "crm.lead.line"
    _description = "Line in CRM Lead"

    @api.depends("price_unit", "product_qty")
    def _compute_expected_revenue(self):
        for rec in self:
            rec.expected_revenue = rec.product_qty * rec.price_unit

    @api.depends("lead_id.probability", "expected_revenue")
    def _compute_prorated_revenue(self):
        for rec in self:
            if rec.lead_id and rec.lead_id.type != "lead":
                rec.prorated_revenue = (
                    rec.expected_revenue * rec.lead_id.probability * (1 / 100)
                )

    lead_id = fields.Many2one("crm.lead", string="Lead")
    name = fields.Char("Description", required=True, translate=True)
    product_id = fields.Many2one("product.product", string="Product", index=True)
    category_id = fields.Many2one(
        "product.category", string="Product Category", index=True
    )
    product_tmpl_id = fields.Many2one(
        "product.template", string="Product Template", index=True
    )
    product_qty = fields.Integer(string="Product Quantity", default=1, required=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", readonly=True)
    price_unit = fields.Float(digits="Product Price")
    company_currency = fields.Many2one(
        "res.currency",
        string="Currency",
        related="lead_id.company_currency",
        readonly=True,
    )
    expected_revenue = fields.Monetary(
        compute="_compute_expected_revenue",
        string="Expected revenue",
        currency_field="company_currency",
        compute_sudo=True,
        store=True,
    )
    prorated_revenue = fields.Monetary(
        compute="_compute_prorated_revenue",
        string="Prorated revenue",
        currency_field="company_currency",
        compute_sudo=True,
        store=True,
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        domain = {}
        if not self.lead_id:
            return
        if not self.product_id:
            self.price_unit = 0.0
            domain["uom_id"] = []
            if self.name and self.name != self.category_id.name:
                self.name = ""
        else:
            product = self.product_id
            self.category_id = product.categ_id.id
            self.product_tmpl_id = product.product_tmpl_id.id
            self.price_unit = product.list_price
            if product.name:
                self.name = product.name
            if (
                not self.uom_id
                or product.uom_id.category_id.id != self.uom_id.category_id.id
            ):
                self.uom_id = product.uom_id.id
            domain["uom_id"] = [("category_id", "=", product.uom_id.category_id.id)]
            if self.uom_id and self.uom_id.id != product.uom_id.id:
                self.price_unit = product.uom_id._compute_price(
                    self.price_unit, self.uom_id
                )
        return {"domain": domain}

    @api.onchange("category_id")
    def _onchange_category_id(self):
        domain = {}
        if not self.lead_id:
            return
        if self.category_id:
            categ_id = self.category_id
            if categ_id.name and not self.name:
                self.name = categ_id.name
            # Check if there are already defined product and product template
            # and remove them if categories do not match
            if self.product_id and self.product_id.categ_id != categ_id:
                self.product_id = None
                self.name = categ_id.name
            if self.product_tmpl_id and self.product_tmpl_id.categ_id != categ_id:
                self.product_tmpl_id = None
        return {"domain": domain}

    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        domain = {}
        if not self.lead_id:
            return
        if self.product_tmpl_id:
            product_tmpl = self.product_tmpl_id
            if product_tmpl.name and not self.name:
                self.name = product_tmpl.name
            self.category_id = product_tmpl.categ_id
            if self.product_id:
                # Check if there are already defined product and remove
                # if it does not match
                if self.product_id.product_tmpl_id != product_tmpl:
                    self.product_id = None
                    self.name = product_tmpl.name
        return {"domain": domain}

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        result = {}
        if not self.uom_id:
            self.price_unit = 0.0
        if self.product_id and self.uom_id:
            price_unit = self.product_id.list_price
            self.price_unit = self.product_id.uom_id._compute_price(
                price_unit, self.uom_id
            )
        return result
