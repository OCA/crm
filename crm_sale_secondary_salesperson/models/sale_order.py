# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("opportunity_id")
    def _onchange_opportunity_id(self):
        if self.opportunity_id:
            self.secondary_user_id = self.opportunity_id.secondary_user_id
