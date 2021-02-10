# Copyright 2021 Eder Brito
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AutomatedActivity(models.Model):
    _name = "crm.automated.activity"
    _description = "Automated Activity for Stages"

    apply_in = fields.Selection(
        selection=[
            ("create", "Creating an Opportunity"),
            ("write", "Changing an Opportunity Stage"),
            ("create_write", "Create Opportunity and Change Stage"),
        ],
        string="Apply In",
        required=True,
        help="Select in which case this rule will be applied",
    )

    crm_stage_id = fields.Many2one(comodel_name="crm.stage", string="Stage",)

    activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Activity Type",
        help="Type for created activities",
        required=True,
    )

    summary = fields.Char(string="Summary", help="Summary for Activity")

    days_deadline = fields.Integer(
        string="Days to Deadline",
        help="The number set here will sum with the current date of the action",
    )

    note = fields.Html(string="Note", help="Note for Activity")

    @api.onchange("activity_type_id")
    def _onchange_activity_type(self):

        self.summary = self.activity_type_id.summary

        self.note = self.activity_type_id.default_description

        if self.activity_type_id.delay_unit == "days":
            self.days_deadline = self.activity_type_id.delay_count

        elif self.activity_type_id.delay_unit == "weeks":
            self.days_deadline = self.activity_type_id.delay_count * 7

        elif self.activity_type_id.delay_unit == "months":
            self.days_deadline = self.activity_type_id.delay_count * 30

    # TODO - Link user_id to future activities, with access rights in Opportunity

    # user_id = fields.Many2one(
    #     comodel_name= 'res.users',
    #     string='User Assigned',
    #     help="If empty, current user will be applied"
    # )
