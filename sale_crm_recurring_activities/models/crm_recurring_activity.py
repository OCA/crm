from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmRecurringActivity(models.Model):
    _name = "crm.recurring.activity"
    _description = "CRM Recurring activity"

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company.id,
        required=True,
    )
    activity_type_id = fields.Many2one(
        "mail.activity.type",
        ondelete="restrict",
        domain="[('res_model', 'in', [False, 'crm.lead'])]",
    )
    user_id = fields.Many2one(
        "res.users",
        string="Assigned to",
        required=True,
    )
    summary = fields.Char(
        compute="_compute_on_activity_type_id",
        store=True,
        readonly=False,
    )
    note = fields.Html(
        sanitize_style=True,
        compute="_compute_on_activity_type_id",
        store=True,
        readonly=False,
    )
    scheduled_days = fields.Integer()

    @api.constrains("user_id", "company_id")
    def _check_user_id(self):
        for rec in self:
            user = rec.user_id
            company = rec.company_id
            if not user or not company:
                continue
            if not user.active or user.share:
                raise ValidationError(
                    _(
                        "You can only assign recurring activities "
                        "to active internal users."
                    )
                )
            if company not in user.company_ids:
                raise ValidationError(
                    _(
                        "Assigned user %(user)s "
                        "does not have access to company: %(company)s.",
                        user=user.display_name,
                        company=company.display_name,
                    )
                )
            if not self.env.user.has_group("sales_team.group_sale_salesman"):
                raise ValidationError(
                    _("The user does not have permission to use the CRM app")
                )

    @api.depends("activity_type_id")
    def _compute_on_activity_type_id(self):
        for activity in self:
            if activity.activity_type_id:
                if activity.activity_type_id.summary:
                    activity.summary = self.activity_type_id.summary
                if activity.activity_type_id.default_note:
                    activity.note = self.activity_type_id.default_note
