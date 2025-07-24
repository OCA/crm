# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmPhonecallReport(models.Model):
    _inherit = "crm.phonecall.report"

    phone_result_id = fields.Many2one("crm.phonecall.result", string="Phone Result")

    def _select(self):
        return super()._select() + ", c.phone_result_id"
