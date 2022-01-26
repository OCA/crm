# Copyright 2022 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class CrmSalespersonPlannerVisitReassignLine(models.Model):
    _name = "crm.salesperson.planner.visit.reassign.line"
    _description = "Salesperson Planner Visit Reassign Line"
    _rec_name = "date"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    date = fields.Date(string="Date", compute="_compute_date", store=True)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        compute="_compute_partner_id",
        store=True,
    )
    visit_state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Validated"),
            ("done", "Visited"),
            ("cancel", "Cancelled"),
            ("incident", "Incident"),
        ],
        compute="_compute_visit_state",
        store=True,
    )
    template_state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("in-progress", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        compute="_compute_template_state",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence", compute="_compute_sequence", store=True
    )
    salesperson_visit_template_id = fields.Many2one(
        string="Template", comodel_name="crm.salesperson.planner.visit.template"
    )
    crm_salesperson_planner_visit_id = fields.Many2one(
        string="Visit", comodel_name="crm.salesperson.planner.visit"
    )

    @api.depends("salesperson_visit_template_id", "crm_salesperson_planner_visit_id")
    def _compute_name(self):
        for sel in self:
            name = ""
            if sel.salesperson_visit_template_id:
                name = sel.salesperson_visit_template_id.name
            elif sel.crm_salesperson_planner_visit_id:
                name = sel.crm_salesperson_planner_visit_id.name
            sel.name = name

    @api.depends("salesperson_visit_template_id", "crm_salesperson_planner_visit_id")
    def _compute_sequence(self):
        for sel in self:
            sequence = ""
            if sel.salesperson_visit_template_id:
                sequence = sel.salesperson_visit_template_id.sequence
            elif sel.crm_salesperson_planner_visit_id:
                sequence = sel.crm_salesperson_planner_visit_id.sequence
            sel.sequence = sequence

    @api.depends("salesperson_visit_template_id", "crm_salesperson_planner_visit_id")
    def _compute_date(self):
        for sel in self:
            date = ""
            if sel.salesperson_visit_template_id:
                date = sel.salesperson_visit_template_id.start_date
            elif sel.crm_salesperson_planner_visit_id:
                date = sel.crm_salesperson_planner_visit_id.date
            sel.date = date

    @api.depends("crm_salesperson_planner_visit_id")
    def _compute_partner_id(self):
        for sel in self:
            partner_id = False
            if sel.crm_salesperson_planner_visit_id:
                partner_id = sel.crm_salesperson_planner_visit_id.partner_id
            sel.partner_id = partner_id

    @api.depends("crm_salesperson_planner_visit_id")
    def _compute_visit_state(self):
        for sel in self:
            visit_state = False
            if sel.crm_salesperson_planner_visit_id:
                visit_state = sel.crm_salesperson_planner_visit_id.state
            sel.visit_state = visit_state

    @api.depends("salesperson_visit_template_id")
    def _compute_template_state(self):
        for sel in self:
            template_state = False
            if sel.salesperson_visit_template_id:
                template_state = sel.salesperson_visit_template_id.state
            sel.template_state = template_state
