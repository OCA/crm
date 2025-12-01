# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Tecnativa - Vicent Cubells
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    claim_count = fields.Integer(string="# Claims", compute="_compute_claim_count")
    claim_ids = fields.One2many(comodel_name="crm.claim", inverse_name="partner_id")

    @api.depends("claim_ids", "child_ids", "child_ids.claim_ids")
    def _compute_claim_count(self):
        partners = self | self.mapped("child_ids")
        partner_data = self.env["crm.claim"]._read_group(
            domain=[("partner_id", "in", partners.ids)],
            groupby=["partner_id"],
            aggregates=["partner_id:count"],
        )
        mapped_data = {p[0].id: p[1] for p in partner_data}
        for partner in self:
            count = mapped_data.get(partner.id, 0)
            for child in partner.child_ids:
                count += mapped_data.get(child.id, 0)
            partner.claim_count = count
