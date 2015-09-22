# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    code = fields.Char(
        string='Claim Number', required=True, default="/", readonly=True,
        oldname='number')

    _sql_constraints = [
        ('crm_claim_unique_code', 'UNIQUE (code, company_id)',
         'The code must be unique per Company!'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).create(vals)

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).copy(default)

    @api.multi
    @api.depends('code')
    def name_get(self):
        orig_names = dict(super(CrmClaim, self).name_get())

        res = []
        for claim in self:
            name = "[{}] {}".format(claim.code, orig_names[claim.id])
            res.append((claim.id, name))
        return res
