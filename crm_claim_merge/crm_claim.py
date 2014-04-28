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

from operator import attrgetter

from openerp.osv import orm
from openerp.tools.translate import _

CRM_CLAIM_FIELDS_TO_MERGE = (
    'action_next',
    'categ_id',
    'cause',
    'company_id',
    'date',
    'date_action_next',
    'date_closed',
    'date_deadline',
    'description',
    'email_cc',
    'email_from',
    'name',
    'partner_id',
    'partner_phone',
    'priority',
    'ref',
    'resolution',
    'section_id',
    'stage_id',
    'state',
    'type_action',
    'user_fault',
    'user_id',
)


class crm_claim(orm.Model):
    _inherit = 'crm.claim'

    def _merge_get_default_main(self, cr, uid, claims, context=None):
        return sorted(claims, key=attrgetter('date'))[0]

    def _merge_check(self, cr, uid, claims, context=None):
        if len(claims) <= 1:
            raise orm.except_orm(
                _('Warning'),
                _('Please select more than one claim from the list view.'))

        partner = next((claim.partner_id for claim in claims), None)
        if partner:
            if any(claim.partner_id != partner for claim in claims
                    if claim.partner_id):
                raise orm.except_orm(
                    _('Error'),
                    _('Cannot merge claims of different partners.'))

    def _merge_fields(self, cr, uid, context=None):
        return CRM_CLAIM_FIELDS_TO_MERGE

    def _merge_data(self, cr, uid, merge_in, claims, fields, context=None):
        """
        Prepare claims data into a dictionary for merging.  Different types
        of fields are processed in different ways:
        - text: all the values are concatenated
        - m2m and o2m: those fields aren't processed
        - m2o: the first not null value prevails (the other are dropped)
        - any other type of field: same as m2o

        :param merge_in: other claims will be merged in this one
        :param claims: list of claims to merge
        :param fields: list of leads' fields to process
        :return data: contains the merged values
        """
        claims = [merge_in] + claims

        def _get_first_not_falsish(attr):
            for claim in claims:
                value = getattr(claim, attr, None)
                if value:
                    return value
            return False

        def _get_first_m2o(attr):
            rel = _get_first_not_falsish(attr)
            return rel.id if rel else False

        def _concat_text(attr):
            return '\n\n'.join([getattr(claim, attr) or '' for claim in claims
                                if hasattr(claim, attr)])

        # Process the fields' values
        data = {}
        for field_name in fields:
            field_info = self._all_columns.get(field_name)
            if field_info is None:
                continue
            field = field_info.column
            if field._type in ('many2many', 'one2many'):
                continue
            elif field._type == 'many2one':
                data[field_name] = _get_first_m2o(field_name)
            elif field._type == 'text':
                data[field_name] = _concat_text(field_name)
            else:
                data[field_name] = _get_first_not_falsish(field_name)

        return data

    def merge(self, cr, uid, ids, merge_in_id=None, context=None):
        """ Merge claims together.

        :param merge_in_ids: the other claims will be merged into this one
            if None, the oldest claim will be selected.
        """
        claims = self.browse(cr, uid, ids, context=context)
        self._merge_check(cr, uid, claims, context=context)
        if merge_in_id is None:
            merge_in = self._merge_get_default_main(cr, uid, claims,
                                                    context=context)
        else:
            for claim in claims[:]:
                if claim.id == merge_in_id:
                    merge_in = claim
                    break
        claims.remove(merge_in)  # keep the tail

        fields = list(self._merge_fields(cr, uid, context=None))
        data = self._merge_data(cr, uid, merge_in, claims,
                                fields, context=context)
        import pdb; pdb.set_trace()
