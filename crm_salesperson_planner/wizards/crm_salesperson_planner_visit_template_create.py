# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields, models
from odoo.exceptions import ValidationError


class CrmSalespersonPlannerVisitTemplateCreate(models.TransientModel):
    _name = "crm.salesperson.planner.visit.template.create"
    _description = "crm salesperson planner visit template create"

    def _default_date_to(self):
        template = self.env["crm.salesperson.planner.visit.template"].browse(
            self.env.context.get("active_id")
        )
        date = template.last_visit_date or fields.Date.context_today(self)
        return date + timedelta(days=7)

    date_to = fields.Date(
        string="Date to", default=lambda self: self._default_date_to(), required=True
    )

    def create_visits(self):
        template = self.env["crm.salesperson.planner.visit.template"].browse(
            self.env.context.get("active_id")
        )
        days = (self.date_to - fields.Date.context_today(self)).days
        if days < 0:
            raise ValidationError(self.env._("The date can't be earlier than today"))
        # Create visits + auto-confirm + auto-done
        template.create_visits(days=days)
        return {"type": "ir.actions.act_window_close"}
