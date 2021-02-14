# Copyright 2021 Eder Brito
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmStage(models.Model):

    _inherit = "crm.stage"

    create_automated_activity = fields.Boolean(string="Create Automatically Activities")

    automated_activity_ids = fields.One2many(
        comodel_name="crm.automated.activity",
        inverse_name="crm_stage_id",
        string="Automated Activities",
    )