from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    crm_recurring_activity_ids = fields.One2many(
        "crm.recurring.activity",
        "company_id",
        string="Recurring Activities",
    )
