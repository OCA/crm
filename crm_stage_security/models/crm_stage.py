# Copyright 2023 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Groups",
        help="If set, only the users of one of those groups will be able to move leads"
        " to this stage.",
    )
