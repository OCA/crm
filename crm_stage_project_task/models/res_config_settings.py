from odoo import fields, models


class ResCompanySettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_stage_project_id = fields.Many2one(
        "project.project", related="company_id.stage_project_id", readonly=False
    )
