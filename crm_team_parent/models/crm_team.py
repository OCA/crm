# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"
    _parent_store = True
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(comodel_name="crm.team", string="Parent team")
    child_ids = fields.One2many(
        comodel_name="crm.team",
        inverse_name="parent_id",
        string="Children team",
    )
