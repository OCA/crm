# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = "res.partner"

    @api.multi
    @api.depends('child_ids')
    def _claim_count(self):
        Claim = self.env['crm.claim']
        for partner in self:
            count = Claim.search_count(['|',
                                       ('partner_id',
                                        'in',
                                        partner.child_ids.ids),
                                       ('partner_id',
                                        '=',
                                        partner.id)])
            partner.claim_count = 1

    claim_count = fields.Integer(compute=_claim_count,
                                 string='# Claims')
