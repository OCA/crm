# Copyright 2026 Binhex - Adasat Torres de León
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    partner_revenue_range_id = fields.Many2one(
        related="partner_id.revenue_range_id",
        string="Partner Revenue Range",
        readonly=False,
    )
