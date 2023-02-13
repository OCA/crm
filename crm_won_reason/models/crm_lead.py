# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    won_reason_id = fields.Many2one("crm.lost.reason")
