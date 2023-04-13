# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    assigned_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Implemented by",
    )
    implemented_partner_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="assigned_partner_id",
        string="Implementation References",
    )
    implemented_count = fields.Integer(
        compute="_compute_implemented_partner_count",
        store=True,
    )

    @api.depends("implemented_partner_ids", "implemented_partner_ids.active")
    def _compute_implemented_partner_count(self):
        for partner in self:
            partner.implemented_count = len(partner.implemented_partner_ids)
