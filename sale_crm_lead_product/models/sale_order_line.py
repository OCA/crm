# Copyright (C) 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    crm_lead_line_id = fields.Many2one("crm.lead.line", copy=False)
