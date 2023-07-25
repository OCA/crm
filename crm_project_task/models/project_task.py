# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "project.task"

    lead_id = fields.Many2one("crm.lead")
