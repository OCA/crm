# Copyright 2021 Sygel - Valentin Vinagre
# Copyright 2021 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmSalespersonPlannerVisitTemplate(models.Model):
    _name = "crm.salesperson.planner.visit.template"
    _description = "Crm Salesperson Planner Visit Template"
    _inherit = "calendar.event"

    name = fields.Char(
        string="Visit Template Number",
        default="/",
        readonly=True,
        copy=False,
    )
    partner_ids = fields.Many2many(
        string="Customer",
        relation="salesperson_planner_res_partner_rel",
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
    user_id = fields.Many2one(
        string="Salesperson",
        tracking=True,
        default=lambda self: self.env.user,
        domain=lambda self: [
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id)
        ],
    )
    categ_ids = fields.Many2many(
        relation="visit_category_rel",
    )
    alarm_ids = fields.Many2many(relation="visit_calendar_event_rel")
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
    rrule_type = fields.Selection(
        default="daily",
        required=True,
    )
    last_visit_date = fields.Date(compute="_compute_last_visit_date", store=True)
    final_date = fields.Date(string="Repeat Until")
    allday = fields.Boolean(default=True)
    recurrency = fields.Boolean(default=True)

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

    @api.constrains("partner_ids")
    def _constrains_partner_ids(self):
        for item in self:
            if len(item.partner_ids) > 1:
                raise ValidationError(_("Only one customer is allowed"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "salesperson.planner.visit.template"
                )
        return super().create(vals_list)

    # overwrite
    # Calling _update_cron from default write funciont is not
    # necessary in this case
    def write(self, vals):
        return super(models.Model, self).write(vals)

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

    def _get_max_date(self):
        return self._increase_date(self.start_date, self.count)

    def _increase_date(self, date, value):
        if self.rrule_type == "daily":
            date += timedelta(days=value)
        elif self.rrule_type == "weekly":
            date += timedelta(weeks=value)
        elif self.rrule_type == "monthly":
            date += timedelta(months=value)
        elif self.rrule_type == "yearly":
            date += timedelta(years=value)
        return date

    def _get_recurrence_dates(self, items):
        dates = []
        max_date = self._get_max_date()
        from_date = self._increase_date(self.last_visit_date or self.start_date, 1)
        if max_date > from_date:
            for _x in range(items):
                if from_date <= max_date:
                    dates.append(from_date)
                    from_date = self._increase_date(from_date, 1)
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
