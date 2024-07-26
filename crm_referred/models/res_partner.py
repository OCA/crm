# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    referred_id = fields.Many2one("crm.referred", string="Referred by")
