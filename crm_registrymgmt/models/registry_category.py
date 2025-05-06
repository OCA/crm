# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RegistryCategory(models.Model):
    _name = 'registry.category'
    _description = "Registry Category"
    _order = 'name'

    name = fields.Char(
        string="Category Name",
        required=True,
        translate=True,
    )
