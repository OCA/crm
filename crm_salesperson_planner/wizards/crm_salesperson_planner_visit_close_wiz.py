# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, fields, models


class CrmSalespersonPlannerVisitCloseWiz(models.TransientModel):
    _name = "crm.salesperson.planner.visit.close.wiz"
    _description = "Get Close Reason"

    def _default_new_date(self):
        visits = self.env["crm.salesperson.planner.visit"].browse(
            self.env.context.get("active_id")
        )
        return visits.date

    def _default_new_sequence(self):
        visits = self.env["crm.salesperson.planner.visit"].browse(
            self.env.context.get("active_id")
        )
        return visits.sequence

    reason_id = fields.Many2one(
        comodel_name="crm.salesperson.planner.visit.close.reason",
        string="Reason",
        required=True,
    )
    image = fields.Image(max_width=1024, max_height=1024)
    new_date = fields.Date(default=lambda self: self._default_new_date())
    new_sequence = fields.Integer(
        string="Sequence",
        help="Used to order Visits in the different views",
        default=lambda self: self._default_new_sequence(),
    )
    require_image = fields.Boolean(
        string="Require Image", related="reason_id.require_image"
    )
    reschedule = fields.Boolean(default=True)
    allow_reschedule = fields.Boolean(
        string="Allow Reschedule", related="reason_id.reschedule"
    )
    notes = fields.Text()

    def action_close_reason_apply(self):
        visits = self.env["crm.salesperson.planner.visit"].browse(
            self.env.context.get("active_id")
        )
        visit_close_find_method_name = "action_%s" % self.reason_id.close_type
        if hasattr(visits, visit_close_find_method_name):
            getattr(visits, visit_close_find_method_name)(
                self.reason_id, self.image, self.notes
            )
            if self.allow_reschedule and self.reschedule:
                visits.copy(
                    {
                        "date": self.new_date,
                        "sequence": self.new_sequence,
                        "opportunity_ids": visits.opportunity_ids.ids,
                    }
                ).action_confirm()
        else:
            raise ValueError(_("The close reason type haven't a function."))
        return {"type": "ir.actions.act_window_close"}
