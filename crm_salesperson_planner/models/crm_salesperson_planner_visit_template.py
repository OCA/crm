# Copyright 2021 Sygel - Valentin Vinagre
# Copyright 2021 Sygel - Manuel Regidor
# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.calendar.models.calendar_recurrence import (
    BYDAY_SELECTION,
    END_TYPE_SELECTION,
    MONTH_BY_SELECTION,
    RRULE_TYPE_SELECTION,
    WEEKDAY_SELECTION,
)


class CrmSalespersonPlannerVisitTemplate(models.Model):
    _name = "crm.salesperson.planner.visit.template"
    _description = "Crm Salesperson Planner Visit Template"
    _inherit = ["mail.thread"]

    # We cannot inherit from calendar.event for several reasons:
    # 1- There are many compute recursion fields that would not allow to change them.
    # 2- Recurrence is only created correctly if the model is calendar.event
    # 3- We want to generate visits ("events") manually when we want and only the ones
    # we want.
    name = fields.Char(
        string="Visit Template Number",
        default="/",
        readonly=True,
        copy=False,
    )
    description = fields.Html()
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        tracking=True,
        default=lambda self: self.env.user,
        domain=lambda self: [
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id)
        ],
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Scheduled by",
        related="user_id.partner_id",
        readonly=True,
    )
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Customer",
        default=False,
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
    categ_ids = fields.Many2many(comodel_name="calendar.event.type", string="Tags")
    alarm_ids = fields.Many2many(
        comodel_name="calendar.alarm",
        string="Reminders",
        ondelete="restrict",
        help="Notifications sent to all attendees to remind of the meeting.",
    )
    state = fields.Selection(
        string="Status",
        required=True,
        copy=False,
        tracking=True,
        selection=[
            ("draft", "Draft"),
            ("in-progress", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
    )
    visit_ids = fields.One2many(
        comodel_name="crm.salesperson.planner.visit",
        inverse_name="visit_template_id",
        string="Visit Template",
    )
    visit_ids_count = fields.Integer(
        string="Number of Sales Person Visits", compute="_compute_visit_ids_count"
    )
    auto_validate = fields.Boolean(default=True)
    last_visit_date = fields.Date(compute="_compute_last_visit_date", store=True)
    final_date = fields.Date(string="Repeat Until")
    start = fields.Datetime(
        required=True,
        tracking=True,
        default=fields.Date.today,
        help="Start date of an event, without time for full days events",
    )
    stop = fields.Datetime(
        required=True,
        tracking=True,
        default=lambda self: fields.Datetime.today() + timedelta(hours=1),
        compute="_compute_stop",
        readonly=False,
        store=True,
        help="Stop date of an event, without time for full days events",
    )
    allday = fields.Boolean(string="All Day", default=True)
    start_date = fields.Date(
        store=True,
        tracking=True,
        compute="_compute_dates",
        inverse="_inverse_dates",
    )
    stop_date = fields.Date(
        string="End Date",
        store=True,
        tracking=True,
        compute="_compute_dates",
        inverse="_inverse_dates",
    )
    duration = fields.Float(compute="_compute_duration", store=True, readonly=False)
    rrule = fields.Char(string="Recurrent Rule")
    rrule_type = fields.Selection(
        RRULE_TYPE_SELECTION,
        string="Recurrence",
        help="Let the event automatically repeat at that interval",
        default="daily",
        required=True,
    )
    event_tz = fields.Selection(_tz_get, string="Timezone")
    end_type = fields.Selection(END_TYPE_SELECTION, string="Recurrence Termination")
    interval = fields.Integer(
        string="Repeat Every", help="Repeat every (Days/Week/Month/Year)"
    )
    count = fields.Integer(string="Repeat", help="Repeat x times")
    mon = fields.Boolean()
    tue = fields.Boolean()
    wed = fields.Boolean()
    thu = fields.Boolean()
    fri = fields.Boolean()
    sat = fields.Boolean()
    sun = fields.Boolean()
    month_by = fields.Selection(MONTH_BY_SELECTION, string="Option")
    day = fields.Integer(string="Date of month")
    weekday = fields.Selection(WEEKDAY_SELECTION)
    byday = fields.Selection(BYDAY_SELECTION)
    until = fields.Date()

    _sql_constraints = [
        (
            "crm_salesperson_planner_visit_template_name",
            "UNIQUE (name)",
            "The visit template number must be unique!",
        ),
    ]

    def _compute_visit_ids_count(self):
        visit_data = self.env["crm.salesperson.planner.visit"].read_group(
            [("visit_template_id", "in", self.ids)],
            ["visit_template_id"],
            ["visit_template_id"],
        )
        mapped_data = {
            m["visit_template_id"][0]: m["visit_template_id_count"] for m in visit_data
        }
        for sel in self:
            sel.visit_ids_count = mapped_data.get(sel.id, 0)

    @api.depends("visit_ids.date")
    def _compute_last_visit_date(self):
        for sel in self.filtered(lambda x: x.visit_ids):
            sel.last_visit_date = sel.visit_ids.sorted(lambda x: x.date)[-1].date

    @api.depends("start", "duration")
    def _compute_stop(self):
        """Same method as in calendar.event."""
        for item in self:
            item.stop = item.start and item.start + timedelta(
                minutes=round((item.duration or 1.0) * 60)
            )
            if item.allday:
                item.stop -= timedelta(seconds=1)

    @api.depends("allday", "start", "stop")
    def _compute_dates(self):
        """Same method as in calendar.event."""
        for item in self:
            if item.allday and item.start and item.stop:
                item.start_date = item.start.date()
                item.stop_date = item.stop.date()
            else:
                item.start_date = False
                item.stop_date = False

    @api.depends("stop", "start")
    def _compute_duration(self):
        """Same method as in calendar.event."""
        for item in self:
            item.duration = self._get_duration(item.start, item.stop)

    def _get_duration(self, start, stop):
        """Same method as in calendar.event."""
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)

    def _inverse_dates(self):
        """Same method as in calendar.event."""
        for item in self:
            if item.allday:
                enddate = fields.Datetime.from_string(item.stop_date)
                enddate = enddate.replace(hour=18)
                startdate = fields.Datetime.from_string(item.start_date)
                startdate = startdate.replace(hour=8)
                item.write(
                    {
                        "start": startdate.replace(tzinfo=None),
                        "stop": enddate.replace(tzinfo=None),
                    }
                )

    @api.constrains("partner_ids")
    def _constrains_partner_ids(self):
        for item in self:
            if len(item.partner_ids) > 1:
                raise ValidationError(_("Only one customer is allowed"))

    @api.onchange("end_type")
    def _onchange_end_type(self):
        """Avoid inconsistent data if you switch from one thing to another."""
        if self.end_type == "count":
            self.until = False
        elif self.end_type == "end_date":
            self.count = 0
        elif self.end_type == "forever":
            self.count = 0
            self.until = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "salesperson.planner.visit.template"
                )
        return super().create(vals_list)

    def action_view_salesperson_planner_visit(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "crm_salesperson_planner.all_crm_salesperson_planner_visit_action"
        )
        action["domain"] = [("id", "=", self.visit_ids.ids)]
        action["context"] = {
            "default_partner_id": self.partner_id.id,
            "default_visit_template_id": self.id,
            "default_description": self.description,
        }
        return action

    def action_validate(self):
        self.write({"state": "in-progress"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_draft(self):
        self.write({"state": "draft"})

    def _prepare_crm_salesperson_planner_visit_vals(self, dates):
        return [
            {
                "partner_id": (
                    fields.first(self.partner_ids).id if self.partner_ids else False
                ),
                "date": date,
                "sequence": self.sequence,
                "user_id": self.user_id.id,
                "description": self.description,
                "company_id": self.company_id.id,
                "visit_template_id": self.id,
            }
            for date in dates
        ]

    # Get the date range from calendar.recurrence, that way the values obtained will
    # be correct (except for incompatible cases).
    def _get_start_range_dates(self):
        """Method to get all dates (sorted) in the range."""
        duration = self.stop - self.start
        ranges = (
            self.env["calendar.recurrence"]
            .new(
                {
                    "rrule_type": self.rrule_type,
                    "interval": self.interval,
                    "month_by": self.month_by,
                    "weekday": self.weekday,
                    "byday": self.byday,
                    "count": self.count,
                    "end_type": self.end_type,
                    "until": self.until,
                    "mon": self.mon,
                    "tue": self.tue,
                    "wed": self.wed,
                    "thu": self.thu,
                    "fri": self.fri,
                    "sat": self.sat,
                    "sun": self.sun,
                }
            )
            ._range_calculation(self, duration)
        )
        start_dates = []
        for start, _stop in ranges:
            start_dates.append(start.date())
        return sorted(start_dates)

    def _get_max_date(self):
        """The maximum date will be the last of the range."""
        return self._get_start_range_dates()[-1]

    def _get_recurrence_dates(self, items):
        """For the n items, get only those that are not already generated."""
        start_dates = self._get_start_range_dates()
        dates = []
        visit_dates = self.visit_ids.mapped("date")
        for _date in start_dates[:items]:
            if _date not in visit_dates:
                dates.append(_date)
        return dates

    def _create_visits(self, days=7):
        return self._prepare_crm_salesperson_planner_visit_vals(
            self._get_recurrence_dates(days)
        )

    def create_visits(self, days=7):
        for item in self:
            visits = self.env["crm.salesperson.planner.visit"].create(
                item._create_visits(days)
            )
            if visits and item.auto_validate:
                visits.action_confirm()
            if item.last_visit_date >= item._get_max_date():
                item.state = "done"

    def _cron_create_visits(self, days=7):
        templates = self.search([("state", "=", "in-progress")])
        templates.create_visits(days)
