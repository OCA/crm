# Copyright 2024 INVITU SARL
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    approval_team_ids = fields.Many2many(
        "crm.team",
        string="Sales Teams opportunities approval",
        readonly=False,
        related="company_id.approval_team_ids",
        help="Choose Sales Teams for which you want opportunity approval",
    )
    approval_tag_ids = fields.Many2many(
        "crm.tag",
        string="CRM Tags opportunities approval",
        readonly=False,
        related="company_id.approval_tag_ids",
        help="Choose CRM tags for which you want opportunity approval",
    )
