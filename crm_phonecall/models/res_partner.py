# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """Added the details of phonecall in the partner."""

    _inherit = "res.partner"

    phonecall_ids = fields.One2many(
        comodel_name="crm.phonecall", inverse_name="partner_id", string="Phonecalls"
    )
    phonecall_count = fields.Integer(compute="_compute_phonecall_count")

    def _compute_phonecall_count(self):
        """Calculate number of phonecalls."""
        partner_data = self.env["crm.phonecall"]._read_group(
            domain=[("partner_id", "in", self.ids)],
            groupby=["partner_id"],
            aggregates=["partner_id:count"],
        )
        mapped_data = {p[0].id: p[1] for p in partner_data}
        for partner in self:
            count = mapped_data.get(partner.id, 0)
            partner.phonecall_count = count
