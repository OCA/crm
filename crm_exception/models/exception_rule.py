# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ExceptionRule(models.Model):
    _inherit = "exception.rule"

    crm_lead_ids = fields.Many2many(comodel_name="crm.lead", string="Opportunities")
    model = fields.Selection(
        selection_add=[
            ("crm.lead", "Lead"),
        ],
        ondelete={"crm.lead": "cascade"},
    )
    stage_ids = fields.Many2many(comodel_name="crm.stage")
