# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2014 Camptocamp SA
#    Merge code freely adapted to claims from merge of crm leads
#    and partners by OpenERP
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
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
from itertools import chain

from openerp import SUPERUSER_ID
from openerp.osv import orm
from openerp.tools.translate import _

CRM_CLAIM_FIELD_BLACKLIST = [
    'message_ids',
    'message_follower_ids',
]


class crm_claim(orm.Model):
    _inherit = 'crm.claim'

    def _merge_get_default_main(self, cr, uid, claims, context=None):
        return sorted(claims, key=attrgetter('date'))[0]

    def _merge_sort(self, cr, uid, claims, context=None):
        """ Sort the tailing claims.

        When claims have concurrent values, the (true-ish) value from the
        first claim is used.
        """
        return sorted(claims, key=attrgetter('date'))

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
        fields = self._all_columns
        fields = (name for name, info in fields.iteritems()
                  if not info.column.readonly)
        fields = (name for name in fields if
                  name not in CRM_CLAIM_FIELD_BLACKLIST)
        return list(fields)

    def _get_fk_on(self, cr, table):
        """ Get all FK pointing to a table """
        q = """  SELECT cl1.relname as table,
                        att1.attname as column
                   FROM pg_constraint as con, pg_class as cl1, pg_class as cl2,
                        pg_attribute as att1, pg_attribute as att2
                  WHERE con.conrelid = cl1.oid
                    AND con.confrelid = cl2.oid
                    AND array_lower(con.conkey, 1) = 1
                    AND con.conkey[1] = att1.attnum
                    AND att1.attrelid = cl1.oid
                    AND cl2.relname = %s
                    AND att2.attname = 'id'
                    AND array_lower(con.confkey, 1) = 1
                    AND con.confkey[1] = att2.attnum
                    AND att2.attrelid = cl2.oid
                    AND con.contype = 'f'
        """
        return cr.execute(q, (table,))

    def _merge_update_foreign_keys(self, cr, uid, merge_in,
                                   claims, context=None):
        claim_ids = [claim.id for claim in claims]

        # find the many2one relation to a claim
        self._get_fk_on(cr, 'crm_claim')

        for table, column in cr.fetchall():
            if 'crm_claim_merge' in table:
                # ignore the wizard tables (TransientModel + relation
                # table)
                continue
            query = ("SELECT column_name FROM information_schema.columns"
                     "  WHERE table_name = %s")
            cr.execute(query, (table, ))
            columns = []
            for data in cr.fetchall():
                if data[0] != column:
                    columns.append(data[0])

            query_dic = {
                'table': table,
                'column': column,
                'value': columns[0],
            }
            if len(columns) <= 1:
                # update of m2m
                query = """
                    UPDATE "%(table)s" as ___tu
                    SET %(column)s = %%s
                    WHERE
                        %(column)s = %%s AND
                        NOT EXISTS (
                            SELECT 1
                            FROM "%(table)s" as ___tw
                            WHERE
                                %(column)s = %%s AND
                                ___tu.%(value)s = ___tw.%(value)s
                        )""" % query_dic
                for claim_id in claim_ids:
                    cr.execute(query, (merge_in.id, claim_id,
                                       merge_in.id))
            else:
                query = ('UPDATE "%(table)s" SET %(column)s = %%s WHERE '
                         '%(column)s IN %%s') % query_dic
                cr.execute(query, (merge_in.id, tuple(claim_ids)))

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

        def _get_first_reference(attr):
            rel = _get_first_not_falsish(attr)
            return '%s,%s' % (rel._model._name, rel.id) if rel else False

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
            field_type = field._type  # noqa
            if field_type in ('many2many', 'one2many'):
                continue
            elif field_type == 'many2one':
                data[field_name] = _get_first_m2o(field_name)
            elif field_type == 'text':
                data[field_name] = _concat_text(field_name)
            elif field_type == 'reference':
                data[field_name] = _get_first_reference(field_name)
            else:
                data[field_name] = _get_first_not_falsish(field_name)

        # Check if the stage is in the stages of the sales team. If not,
        # assign the stage with the lowest sequence
        if data.get('section_id'):
            stage_obj = self.pool['crm.case.stage']
            section_stage_ids = stage_obj.search(
                cr, uid,
                [('section_ids', 'in', data['section_id'])],
                order='sequence',
                context=context)
            if data.get('stage_id') not in section_stage_ids:
                data['stage_id'] = (section_stage_ids[0] if
                                    section_stage_ids else False)
        return data

    def _merge_claim_history(self, cr, uid, merge_in, claims, context=None):
        merge_in_id = merge_in.id
        for claim in claims:
            history_ids = set()
            for history in claim.message_ids:
                history_ids.add(history.id)
            message = self.pool['mail.message']
            message.write(cr, uid,
                          list(history_ids),
                          {'res_id': merge_in_id,
                           'subject': _("From %s") % claim.name_get()[0][1],
                           },
                          context=context)

    def _merge_claim_attachments(self, cr, uid, merge_in, claims, context=None):
        attach_obj = self.pool['ir.attachment']

        # return attachments of claims
        def _get_attachments(claim_id):
            attachment_ids = attach_obj.search(
                cr, uid,
                [('res_model', '=', self._name),
                 ('res_id', '=', claim_id)],
                context=context)
            return attach_obj.browse(cr, uid, attachment_ids, context=context)

        first_attachments = _get_attachments(merge_in.id)
        merge_in_id = merge_in.id

        # Counter of all attachments to move.
        # Used to make sure the name is different for all attachments
        existing_names = [att.name for att in first_attachments]
        for claim in claims:
            attachments = _get_attachments(claim.id)
            for attachment in attachments:
                values = {'res_id': merge_in_id}
                name = attachment.name
                count = 1
                while name in existing_names:
                    name = "%s (%s)" % (attachment.name, count)
                    count += 1
                values['name'] = name
                attachment.write(values)
                existing_names.append(name)

    def _merge_mail_body(self, cr, uid, claim, fields, title=False, context=None):
        body = []
        if title:
            body.append("%s\n" % title)

        for field_name in fields:
            field_info = self._all_columns.get(field_name)
            if field_info is None:
                continue
            field = field_info.column
            value = ''

            field_type = field._type  # noqa

            if field_type == 'selection':
                if hasattr(field.selection, '__call__'):
                    key = field.selection(self, cr, uid, context=context)
                else:
                    key = field.selection
                value = dict(key).get(claim[field_name], claim[field_name])
            elif field_type in ('many2one', 'reference'):
                if claim[field_name]:
                    value = claim[field_name].name_get()[0][1]
            elif field_type in ('many2many', 'one2many'):
                if claim[field_name]:
                    for val in claim[field_name]:
                        field_value = val.name_get()[0][1]
                        value += field_value + ","
            else:
                value = claim[field_name]

            body.append("%s: %s" % (field.string, value or ''))
        return "<br/>".join(body + ['<br/>'])

    def _merge_notify(self, cr, uid, merge_in, claims, context=None):
        """ Create a message gathering merged claims information.  """
        details = []
        subject = [_('Merged claims')]
        for claim in chain([merge_in] + claims):
            name = claim.name_get()[0][1]
            subject.append(name)
            title = "%s: %s" % (_('Merged claim'), name)
            fields = list(self._merge_fields(cr, uid, context=context))
            details.append(self._merge_mail_body(cr, uid, claim, fields,
                                                 title=title, context=context))

        # Chatter message's subject
        subject = subject[0] + ": " + ", ".join(subject[1:])
        details = "\n\n".join(details)
        return self.message_post(cr, uid, [merge_in.id],
                                 body=details, subject=subject,
                                 context=context)

    def _merge_followers(self, cr, uid, merge_in, claims, context=None):
        """ Subscribe the same followers on the final claim. """
        follower_ids = [fol.id for fol in merge_in.message_follower_ids]

        fol_obj = self.pool.get('mail.followers')
        fol_ids = fol_obj.search(
            cr, SUPERUSER_ID,
            [('res_model', '=', self._name),
             ('res_id', 'in', [claim.id for claim in claims])],
            context=context)

        for fol in fol_obj.browse(cr, SUPERUSER_ID, fol_ids, context=context):
            if fol.res_id in follower_ids:
                continue
            subtype_ids = [st.id for st in fol.subtype_ids]
            self.message_subscribe(cr, SUPERUSER_ID, [merge_in.id],
                                   [fol.partner_id.id],
                                   subtype_ids=subtype_ids,
                                   context=context)

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
            for claim in claims:
                if claim.id == merge_in_id:
                    merge_in = claim
                    break
        claims.remove(merge_in)  # keep the tail
        claims = self._merge_sort(cr, uid, claims, context=context)

        fields = list(self._merge_fields(cr, uid, context=None))
        data = self._merge_data(cr, uid, merge_in, claims,
                                fields, context=context)

        self._merge_claim_history(cr, uid, merge_in, claims, context=context)
        self._merge_claim_attachments(cr, uid, merge_in, claims,
                                      context=context)

        self._merge_notify(cr, uid, merge_in, claims, context=context)
        self._merge_followers(cr, uid, merge_in, claims, context=context)

        self._merge_update_foreign_keys(cr, uid, merge_in,
                                        claims, context=context)
        # Write merged data into first claim
        self.write(cr, uid, [merge_in.id], data, context=context)

        # Delete tail claims
        # We use the SUPERUSER to avoid access rights issues because as
        # the user had the rights to see the records it should be safe
        # to do so
        self.unlink(cr, SUPERUSER_ID,
                    [claim.id for claim in claims],
                    context=context)

        return merge_in.id
