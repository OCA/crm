# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmReferred(models.Model):
    _name = "crm.referred"
    _description = "Lead/opportunity referred by categorized"

    name = fields.Char(required=True, translate=True)
