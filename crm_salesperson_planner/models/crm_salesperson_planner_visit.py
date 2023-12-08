# Copyright 2021 Sygel - Valentin Vinagre
# Copyright 2021 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmSalespersonPlannerVisit(models.Model):
    _name = "crm.salesperson.planner.visit"
    _description = "Salesperson Planner Visit"
    _order = "date desc,sequence"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Visit Number",
        required=True,
        default="/",
        readonly=True,
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
    )
    partner_phone = fields.Char(string="Phone", related="partner_id.phone")
    partner_mobile = fields.Char(string="Mobile", related="partner_id.mobile")
    date = fields.Date(
        default=fields.Date.context_today,
        required=True,
    )
    sequence = fields.Integer(
        help="Used to order Visits in the different views",
        default=20,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        index=True,
        tracking=True,
        default=lambda self: self.env.user,
        domain=lambda self: [
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id)
        ],
    )
    opportunity_ids = fields.Many2many(
        comodel_name="crm.lead",
        relation="crm_salesperson_planner_visit_crm_lead_rel",
        string="Opportunities",
        copy=False,
        domain="[('type', '=', 'opportunity'), ('partner_id', 'child_of', partner_id)]",
    )
    description = fields.Html()
    state = fields.Selection(
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Validated"),
            ("done", "Visited"),
            ("cancel", "Cancelled"),
            ("incident", "Incident"),
        ],
        default="draft",
    )
    close_reason_id = fields.Many2one(
        comodel_name="crm.salesperson.planner.visit.close.reason", string="Close Reason"
    )
    close_reason_image = fields.Image(max_width=1024, max_height=1024, attachment=True)
    close_reason_notes = fields.Text()
    visit_template_id = fields.Many2one(
        comodel_name="crm.salesperson.planner.visit.template", string="Visit Template"
    )
    calendar_event_id = fields.Many2one(
        comodel_name="calendar.event", string="Calendar Event"
    )

    _sql_constraints = [
        (
            "crm_salesperson_planner_visit_name",
            "UNIQUE (name)",
            "The visit number must be unique!",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "salesperson.planner.visit"
                )
        return super().create(vals_list)

    def action_draft(self):
        if self.state not in ["cancel", "incident", "done"]:
            raise ValidationError(
                _("The visit must be in cancelled, incident or visited state")
            )
        if self.calendar_event_id:
            self.calendar_event_id.with_context(bypass_cancel_visit=True).unlink()
        self.write({"state": "draft"})

    def action_confirm(self):
        if self.filtered(lambda a: not a.state == "draft"):
            raise ValidationError(_("The visit must be in draft state"))
        events = self.create_calendar_event()
        if events:
            self.browse(events.mapped("res_id")).write({"state": "confirm"})

    def action_done(self):
        if not self.state == "confirm":
            raise ValidationError(_("The visit must be in confirmed state"))
        self.write({"state": "done"})

    def action_cancel(self, reason_id, image=None, notes=None):
        if self.state not in ["draft", "confirm"]:
            raise ValidationError(_("The visit must be in draft or validated state"))
        if self.calendar_event_id:
            self.calendar_event_id.with_context(bypass_cancel_visit=True).unlink()
        self.write(
            {
                "state": "cancel",
                "close_reason_id": reason_id.id,
                "close_reason_image": image,
                "close_reason_notes": notes,
            }
        )

    def _prepare_calendar_event_vals(self):
        return {
            "name": self.name,
            "partner_ids": [(6, 0, [self.partner_id.id, self.user_id.partner_id.id])],
            "user_id": self.user_id.id,
            "start_date": self.date,
            "stop_date": self.date,
            "start": self.date,
            "stop": self.date,
            "allday": True,
            "res_model": self._name,
            "res_model_id": self.env.ref(
                "crm_salesperson_planner.model_crm_salesperson_planner_visit"
            ).id,
            "res_id": self.id,
        }

    def create_calendar_event(self):
        events = self.env["calendar.event"]
        for item in self:
            event = self.env["calendar.event"].create(
                item._prepare_calendar_event_vals()
            )
            if event:
                # Since this commit https://github.com/odoo/odoo/commit/
                # 71dc58acfcc4589bc5996b48e157aea6b0f8a609 Odoo remove the event
                # calendar linked to a mail activity. To avoid Odoo remove the calendar
                # event we disassociate the event and activity.
                event.activity_ids.calendar_event_id = False
                event.activity_ids.unlink()
                item.calendar_event_id = event
            events += event
        return events

    def action_incident(self, reason_id, image=None, notes=None):
        if self.state not in ["draft", "confirm"]:
            raise ValidationError(_("The visit must be in draft or validated state"))
        self.write(
            {
                "state": "incident",
                "close_reason_id": reason_id.id,
                "close_reason_image": image,
                "close_reason_notes": notes,
            }
        )

    def unlink(self):
        if any(sel.state not in ["draft", "cancel"] for sel in self):
            raise ValidationError(_("Visits must be in cancelled state"))
        return super().unlink()

    def write(self, values):
        ret_val = super().write(values)
        if (values.get("date") or values.get("user_id")) and not self.env.context.get(
            "bypass_update_event"
        ):
            new_vals = {}
            for item in self.filtered(lambda a: a.calendar_event_id):
                if values.get("date"):
                    new_vals["start"] = values.get("date")
                    new_vals["stop"] = values.get("date")
                if values.get("user_id"):
                    new_vals["user_id"] = values.get("user_id")
                item.calendar_event_id.write(new_vals)
        return ret_val
