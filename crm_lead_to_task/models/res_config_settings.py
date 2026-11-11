from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crm_archive_lead_on_convert = fields.Boolean(
        related="company_id.crm_archive_lead_on_convert", readonly=False
    )
    crm_force_project_id = fields.Many2one(
        related="company_id.crm_force_project_id", readonly=False
    )
