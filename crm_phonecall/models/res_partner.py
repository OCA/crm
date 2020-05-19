# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    """Added the details of phonecall in the partner."""

    _inherit = "res.partner"

    phonecall_ids = fields.One2many(
        comodel_name='crm.phonecall',
        inverse_name='partner_id',
        string='Phonecalls',
    )
    phonecall_count = fields.Integer(
        compute='_compute_phonecall_count',
    )

    @api.multi
    def _compute_phonecall_count(self):
        """Calculate number of phonecalls."""
        for partner in self:
            partner.phonecall_count = self.env[
                'crm.phonecall'].search_count(
                [('partner_id', '=', partner.id)])
