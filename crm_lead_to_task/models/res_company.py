from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    crm_archive_lead_on_convert = fields.Boolean(default=True)
    crm_force_project_id = fields.Many2one("project.project", "Force Project")
