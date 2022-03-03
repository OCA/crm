# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmLostReason(models.Model):
    _inherit = "crm.lost.reason"

    reason_type = fields.Selection([("won", "Won"), ("lost", "Lost")], default="lost")
