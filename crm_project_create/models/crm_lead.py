# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    project_id = fields.Many2one("project.project", string="Project")
