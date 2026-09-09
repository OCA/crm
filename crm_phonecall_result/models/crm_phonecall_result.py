# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmPhonecallResult(models.Model):
    _name = "crm.phonecall.result"
    _description = "Phonecall Result"
    _order = "priority"

    name = fields.Char(required=True, translate=True)
    description = fields.Text()
    priority = fields.Integer(default=10)

    _name_uniq = models.Constraint(
        "unique (name)",
        "Name must be unique",
    )

    def copy(self, default=None):
        default = dict(default or {})
        if "name" not in default:
            default["name"] = self.env._("%s (Copy)", self.name)
        return super().copy(default=default)
