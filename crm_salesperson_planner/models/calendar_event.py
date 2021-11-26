# Copyright 2021 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    salesperson_planner_visit_ids = fields.One2many(
        string="Salesperson Visits",
        comodel_name="crm.salesperson.planner.visit",
        inverse_name="calendar_event_id",
    )

    def write(self, values):
        if values.get("start") or values.get("user_id"):
            salesperson_visit_events = self.filtered(
                lambda a: a.res_model == "crm.salesperson.planner.visit"
            )
            if salesperson_visit_events:
                new_vals = {}
                if values.get("start"):
                    new_vals["date"] = values.get("start")
                if values.get("user_id"):
                    new_vals["user_id"] = values.get("user_id")
                    user_id = self.env["res.users"].browse(values.get("user_id"))
                    if user_id:
                        partner_ids = self.partner_ids.filtered(
                            lambda a: a != self.user_id.partner_id
                        ).ids
                        partner_ids.append(user_id.partner_id.id)
                        values["partner_ids"] = [(6, 0, partner_ids)]
                salesperson_visit_events.mapped(
                    "salesperson_planner_visit_ids"
                ).with_context(bypass_update_event=True).write(new_vals)
        return super(CalendarEvent, self).write(values)

    def unlink(self, can_be_deleted=True):
        if not self.env.context.get("bypass_cancel_visit"):
            salesperson_visit_events = self.filtered(
                lambda a: a.res_model == "crm.salesperson.planner.visit"
                and a.salesperson_planner_visit_ids
            )
            if salesperson_visit_events:
                error_msg = ""
                for event in salesperson_visit_events:
                    error_msg += _(
                        "Event %s is related to salesperson visit %s. "
                        "Cancel it to delete this event.\n"
                    ) % (event.name, event.salesperson_planner_visit_ids[0].name)
                raise ValidationError(error_msg)
        return super(CalendarEvent, self).unlink(can_be_deleted)
