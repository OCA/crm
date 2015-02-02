# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _


class crm_claim_merge(orm.TransientModel):
    """ Merge claims together.  """

    _name = 'crm.claim.merge'
    _description = 'Merge Claims'
    _columns = {
        'claim_ids': fields.many2many('crm.claim',
                                      string='Claims'),
        'merge_in_id': fields.many2one(
            'crm.claim',
            string='Merge in',
            domain="[('id', 'in', claim_ids[0][2])]",
            help="The other claims will be merged "
                 "into this one."),
    }

    def redirect_new_claim(self, cr, uid, claim_id, context=None):
        models_data = self.pool.get('ir.model.data')
        __, form_view = models_data.get_object_reference(
            cr, uid, 'crm_claim', 'crm_case_claims_form_view')
        return {
            'name': _('Claim'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.claim',
            'res_id': int(claim_id),
            'view_id': form_view,
            'type': 'ir.actions.act_window',
        }

    def action_merge(self, cr, uid, ids, context=None):
        claim_obj = self.pool['crm.claim']
        if isinstance(ids, (tuple, list)):
            assert len(ids) == 1, "Expect 1 ID, got: %s" % ids
            ids = ids[0]
        wizard = self.browse(cr, uid, ids, context=context)
        merge_ids = [claim.id for claim in wizard.claim_ids]
        merged_id = claim_obj.merge(cr, uid, merge_ids,
                                    merge_in_id=wizard.merge_in_id.id,
                                    context=context)
        return self.redirect_new_claim(cr, uid, merged_id, context=context)

    def default_get(self, cr, uid, field_list, context=None):
        """
        Use active_ids from the context to fetch the claims to merge.
        """
        if context is None:
            context = {}
        res = super(crm_claim_merge, self).default_get(
            cr, uid, field_list, context=context)
        if 'claim_ids' in field_list:
            res['claim_ids'] = claim_ids = context.get('active_ids')
            if 'merge_in_id' in field_list and claim_ids:
                claim_obj = self.pool['crm.claim']
                claims = claim_obj.browse(cr, uid, claim_ids, context=context)
                res['merge_in_id'] = claim_obj._merge_get_default_main(
                    cr, uid, claims, context=context).id
        return res
