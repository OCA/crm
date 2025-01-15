# Copyright 2024 INVITU SARL
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    approval_team_ids = fields.Many2many("crm.team")
    approval_tag_ids = fields.Many2many("crm.tag")
