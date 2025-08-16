from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    stage_project_id = fields.Many2one(
        "project.project",
        required=True,
        ondelete="cascade",
        string="CRM State Default Project",
    )
