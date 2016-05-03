# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openerp import _, api, fields, models


class CrmClaimMerge(models.TransientModel):
    """ Merge claims together.  """

    _name = 'crm.claim.merge'
    _description = 'Merge Claims'

    claims = fields.Many2many(
        comodel_name='crm.claim',
        string='Claims')

    base_claim = fields.Many2one(
        comodel_name='crm.claim',
        string='Base Claim',
        domain="[('id', 'in', claims[0][2])]",
        help="The other claims will be merged "
             "into this one.")

    @api.multi
    def redirect_new_claim(self):
        form_view = self.env.ref('crm_claim.crm_case_claims_form_view')
        return {
            'name': _('Claim'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.claim',
            'res_id': self.base_claim.id,
            'view_id': form_view.id,
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def action_merge(self):
        self.ensure_one()
        self.claims.merge(self.base_claim)
        return self.redirect_new_claim()

    @api.model
    def default_get(self, field_list):
        """
        Use active_ids from the context to fetch the claims to merge.
        """
        res = super(CrmClaimMerge, self).default_get(field_list)
        claim_obj = self.env['crm.claim']
        if 'claims' in field_list:
            res['claims'] = self.env.context.get('active_ids')
            claims = claim_obj.browse(res['claims'])
            if 'base_claim' in field_list and claims:
                res['base_claim'] = claims._merge_get_default_base().id
        return res
