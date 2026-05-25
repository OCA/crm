# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    project_id = fields.Many2one("project.project", string="Project")

    def toggle_active(self):
        """Archive or reactivate the project and their analytic account
        on lead toggle."""
        res = super().toggle_active()
        for lead in self.filtered(lambda lead: lead.project_id):
            lead.sudo().project_id.active = lead.active
            lead.sudo().project_id.analytic_account_id.active = lead.active
        return res
