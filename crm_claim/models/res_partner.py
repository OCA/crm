# -*- coding: utf-8 -*-
# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    claim_count = fields.Integer(
        string='# Claims',
        compute='_compute_claim_count',
    )

    @api.model
    def _compute_claim_count(self):
        partners = self | self.mapped('child_ids')
        partner_data = self.env['crm.claim'].read_group(
            [('partner_id', 'in', partners.ids)],
            ['partner_id'],
            ['partner_id'],
        )
        mapped_data = dict(
            [(m['partner_id'][0], m['partner_id_count']) for m in partner_data]
        )
        for partner in self:
            partner.claim_count = mapped_data.get(partner.id, 0)
