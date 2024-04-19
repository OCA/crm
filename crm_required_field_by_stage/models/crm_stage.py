# Copyright 2024 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    required_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        domain=[("model", "=", "crm.lead")],
        help="Fields that are required when the lead is in this stage.",
    )
