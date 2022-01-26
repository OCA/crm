# Copyright 2022 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmSalespersonPlannerVisitReassign(models.Model):
    _name = "crm.salesperson.planner.visit.reassign"
    _description = "Salesperson Planner Visit Reassign"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", default="/", readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("validated", "Validated"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        readonly=True,
        copy=False,
        tracking=True,
        default="draft",
    )
    salesperson_reassign_line_ids = fields.Many2many(
        comodel_name="crm.salesperson.planner.visit.reassign.line",
        string="Reassign Lines",
        relation="salesperson_reassign_rel",
    )
    visit_reassign_line_ids = fields.Many2many(
        comodel_name="crm.salesperson.planner.visit.reassign.line",
        string="Reassign Lines",
        relation="visit_reassign_rel",
    )
    search_visits = fields.Boolean(string="Search Visits", default=True)
    search_templates = fields.Boolean(string="Search Templates")
    done_date = fields.Date(string="Done Date", readonly=True)
    current_user_id = fields.Many2one(
        string="Salesperson", comodel_name="res.users", required=True
    )
    new_user_id = fields.Many2one(string="New Salesperson", comodel_name="res.users")
    start_date = fields.Date(
        string="Start Date",
        help="* If both start date and end date are selected, "
        "visits will be searched using that range.\n"
        "* If both start date and end date are left unselected, "
        "visits will be searched regardless date",
    )
    end_date = fields.Date(string="End Date")
    template_draft_state = fields.Boolean(string="Draft", default=True)
    template_in_progress_state = fields.Boolean(string="In Progress", default=True)
    template_done_state = fields.Boolean(string="Done")
    template_cancel_state = fields.Boolean(string="Cancelled")
    visit_draft_state = fields.Boolean(string="Draft", default=True)
    visit_confirm_state = fields.Boolean(string="Validated", default=True)
    visit_done_state = fields.Boolean(string="Done")
    visit_cancel_state = fields.Boolean(string="Cancel")
    visit_incident_state = fields.Boolean(string="Incident")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "salesperson.planner.reassign"
                )
        return super().create(vals_list)

    def get_template_states(self):
        template_states = []
        if self.template_draft_state:
            template_states.append("draft")
        if self.template_in_progress_state:
            template_states.append("in-progress")
        if self.template_done_state:
            template_states.append("done")
        if self.template_cancel_state:
            template_states.append("cancel")
        return template_states

    def get_visit_states(self):
        visit_states = []
        if self.visit_draft_state:
            visit_states.append("draft")
        if self.visit_confirm_state:
            visit_states.append("confirm")
        if self.visit_done_state:
            visit_states.append("done")
        if self.visit_cancel_state:
            visit_states.append("cancel")
        if self.visit_incident_state:
            visit_states.append("incident")
        return visit_states

    def action_search(self):
        self.salesperson_reassign_line_ids.unlink()
        self.visit_reassign_line_ids.unlink()
        lines = []
        if self.search_templates:
            template_states = self.get_template_states()
            if template_states:
                template_ids = self.env[
                    "crm.salesperson.planner.visit.template"
                ].search(
                    [
                        ("user_id", "=", self.current_user_id.id),
                        ("state", "in", template_states),
                    ]
                )
                for t in template_ids:
                    lines.append({"salesperson_visit_template_id": t.id})
        if self.search_visits:
            visit_states = self.get_visit_states()
            if visit_states:
                visits_search = [
                    ("user_id", "=", self.current_user_id.id),
                    ("state", "in", visit_states),
                ]
                if self.start_date:
                    visits_search.append(("date", ">=", self.start_date))
                if self.end_date:
                    visits_search.append(("date", "<=", self.end_date))
                visit_ids = self.env["crm.salesperson.planner.visit"].search(
                    visits_search
                )
                for v in visit_ids:
                    lines.append({"crm_salesperson_planner_visit_id": v.id})
        if lines:
            reassign_lines = self.env[
                "crm.salesperson.planner.visit.reassign.line"
            ].create(lines)
            self.write(
                {
                    "visit_reassign_line_ids": [
                        (
                            6,
                            0,
                            reassign_lines.filtered(
                                lambda a: a.crm_salesperson_planner_visit_id
                            ).ids,
                        )
                    ],
                    "salesperson_reassign_line_ids": [
                        (
                            6,
                            0,
                            reassign_lines.filtered(
                                lambda a: a.salesperson_visit_template_id
                            ).ids,
                        )
                    ],
                }
            )

    def action_validate(self):
        if not self.new_user_id:
            raise ValidationError(_("Please, select a new Salesperson."))
        self.write({"state": "validated"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_to_draft(self):
        self.write({"state": "draft"})

    def action_reassign(self):
        if not self.new_user_id:
            raise ValidationError(_("Please, select a new Salesperson."))
        tmpl_chng = False
        visits_changed = False
        if self.search_templates:
            tmpl_chng = self.salesperson_reassign_line_ids.filtered(
                lambda a: a.salesperson_visit_template_id.user_id
                != self.current_user_id
                or a.salesperson_visit_template_id.state
                not in self.get_template_states()
            )
            if not tmpl_chng:
                self.salesperson_reassign_line_ids.salesperson_visit_template_id.write(
                    {"user_id": self.new_user_id.id}
                )
        if self.search_visits:
            visits_changed = self.visit_reassign_line_ids.filtered(
                lambda a: a.crm_salesperson_planner_visit_id.user_id
                != self.current_user_id
                or a.crm_salesperson_planner_visit_id.state
                not in self.get_visit_states()
                or (
                    a.crm_salesperson_planner_visit_id.date < self.start_date
                    if self.start_date
                    else False
                )
                or (
                    a.crm_salesperson_planner_visit_id.date > self.end_date
                    if self.end_date
                    else False
                )
            )
            if not visits_changed:
                self.visit_reassign_line_ids.crm_salesperson_planner_visit_id.write(
                    {"user_id": self.new_user_id.id}
                )
        error_msg = ""
        if self.search_templates and tmpl_chng:
            error_msg += _("\nThe following templates have changed:\n")
            for t in tmpl_chng:
                error_msg += "%s\n" % t.salesperson_visit_template_id.name
        if self.search_visits and visits_changed:
            error_msg += _("\nThe following visits have changed:\n")
            for t in visits_changed:
                error_msg += "%s\n" % t.crm_salesperson_planner_visit_id.name
        if error_msg != "":
            error_msg += _(
                "\n Please, send the reassignation to Draft state, "
                "search for visits/templates and try reassigning again."
            )
            raise ValidationError(error_msg)
        self.write({"state": "done", "done_date": fields.Datetime.now()})
