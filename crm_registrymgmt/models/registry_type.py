# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RegistryType(models.Model):
    _name = 'registry.type'
    _description = "Registry Type"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
        translate=True,
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique !')
    ]
