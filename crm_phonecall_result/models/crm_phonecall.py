# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CRMPhonecall(models.Model):
    _inherit = "crm.phonecall"

    phone_result_id = fields.Many2one(
        comodel_name="crm.phonecall.result",
        string="Result call",
    )
