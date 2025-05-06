# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RegistryChannel(models.Model):
    _name = 'registry.channel'
    _description = "Registry channel"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
