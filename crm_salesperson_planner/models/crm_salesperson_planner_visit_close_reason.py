# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmSalespersonPlannerVisitCloseReason(models.Model):
    _name = "crm.salesperson.planner.visit.close.reason"
    _description = "SalesPerson Planner Visit Close Reason"

    name = fields.Char(string="Description", required=True, translate=True)
    close_type = fields.Selection(
        selection=[("cancel", "Cancel"), ("incident", "Incident")],
        string="Type",
        required=True,
        default="cancel",
    )
    require_image = fields.Boolean(string="Require Image", default=False)
    reschedule = fields.Boolean(string="Reschedule", default=False)
