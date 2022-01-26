# Copyright 2022 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmSalespersonPlannerVisit(models.Model):
    _inherit = "crm.salesperson.planner.visit"

    last_user_id = fields.Many2one(comodel_name="res.users", string="Last Salesperson",)

    def write(self, vals):
        if (
            not self.env.context.get("bypass_update_event")
            and vals.get("user_id")
            and self.user_id
            and (not self.last_user_id or self.last_user_id != vals["user_id"])
        ):
            vals["last_user_id"] = self.user_id.id
        return super().write(vals)
