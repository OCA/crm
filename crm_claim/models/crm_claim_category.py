# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Tecnativa - Vicent Cubells
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CrmClaimCategory(models.Model):
    _name = "crm.claim.category"
    _description = "Category of claim"

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Sales Team',
    )
