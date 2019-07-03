# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmStage(models.Model):

    _inherit = 'crm.stage'

    active = fields.Boolean(default=True)
