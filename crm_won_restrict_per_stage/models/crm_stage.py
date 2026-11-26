# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    show_won_button = fields.Boolean(default=True)
