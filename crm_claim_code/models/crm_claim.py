# -*- coding: utf-8 -*-
# Copyright 2015 Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 AvanzOsc (http://www.avanzosc.es)
# Copyright 2017 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class CrmClaim(models.Model):
    _inherit = "crm.claim"
    _rec_name = 'display_name'

    code = fields.Char(
        string='Claim Number',
        required=True,
        default="/",
        readonly=True,
        copy=False,
    )
    display_name = fields.Char(
        compute='compute_display_name',
        store=True
    )

    _sql_constraints = [
        ('crm_claim_unique_code', 'UNIQUE (code)',
         'The code must be unique!'),
    ]

    @api.model
    def create(self, values):
        if values.get('code', '/') == '/':
            values['code'] = self.env['ir.sequence'].next_by_code('crm.claim')
        return super(CrmClaim, self).create(values)

    @api.multi
    @api.depends('name', 'code')
    def compute_display_name(self):
        for rec in self:
            if rec.name and rec.code:
                rec.display_name = u'[%s] %s' % (rec.code, rec.name)
