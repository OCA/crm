# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from operator import attrgetter
from itertools import chain

from openerp import _, api, models
from openerp.exceptions import UserError

CRM_CLAIM_FIELD_BLACKLIST = [
    'message_ids',
    'message_follower_ids',
]


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    def _merge_get_default_base(self):
        """ From the whole selection of claims, return the main claim.

        The main claim will be the claim in which the others (tail
        claims) will be merged.
        """
        return self.sorted(key=attrgetter('date'))[0]

    @api.multi
    def _merge_sort(self):
        """ Sort the tail claims.

        The tail claims are the selection of claims but the main claim.
        The sorting of the tail claim will determine what the priority
        is when several claims have a value for a field: the first in
        the list will have its value kept.
        """
        return self.sorted(key=attrgetter('date'))

    @api.multi
    def _merge_check(self):

        if len(self) <= 1:
            raise UserError(
                _('Please select more than one claim from the list view.'))

        partner = next((claim.partner_id for claim in self), None)
        if partner:
            if any(claim.partner_id != partner for claim in self
                    if claim.partner_id):
                raise UserError(
                    _('Cannot merge claims of different partners.'))

    @api.model
    def _merge_fields(self):
        fields = self._all_columns
        fields = (name for name, info in fields.iteritems()
                  if not info.column.readonly)
        fields = (name for name in fields if
                  name not in CRM_CLAIM_FIELD_BLACKLIST)
        return list(fields)

    @api.multi
    def _get_fk_on(self, cursor, table):
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
        cursor.execute(q, (table,))
        return cursor.fetchall()

    @api.multi
    def _merge_update_foreign_keys(self, base_claim):
        cursor = self.env.cr

        # find the many2one relation to a claim
        for table, column in self._get_fk_on(cursor, 'crm_claim'):
            if 'crm_claim_merge' in table:
                # ignore the wizard tables (TransientModel + relation
                # table)
                continue
            query = ("SELECT column_name FROM information_schema.columns"
                     "  WHERE table_name = %s")
            cursor.execute(query, (table, ))
            columns = []
            for data in cursor.fetchall():
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
                for claim_id in self.ids:
                    cursor.execute(
                        query,
                        (base_claim.id, claim_id, base_claim.id)
                    )
            else:
                query = ('UPDATE "%(table)s" SET %(column)s = %%s WHERE '
                         '%(column)s IN %%s') % query_dic
                cursor.execute(query, (base_claim.id, tuple(self.ids)))

    @api.multi
    def _merge_data(self, base_claim, fields):
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
        claims = base_claim | self
        # Re-sort claims after union
        claims = claims._merge_sort()

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

        # Check if the stage is in the stages of the sales team or default.
        # If not, assign the stage with the lowest sequence
        stage_obj = self.env['crm.claim.stage']
        team_stages = stage_obj.search(
            ['|',
             ('team_ids', 'in', data['team_id']),
             ('case_default', '=', True)],
            order='sequence')
        if data.get('stage_id') not in team_stages.ids:
            data['stage_id'] = (team_stages[0].id if
                                team_stages else False)
        return data

    @api.multi
    def _merge_claim_history(self, base_claim):
        for claim in self:
            claim.message_ids.write({
                'res_id': base_claim.id,
                'subject': _("From %s") % claim.name_get()[0][1],
            })

    @api.multi
    def _merge_claim_attachments(self, base_claim):
        attach_obj = self.env['ir.attachment']

        # return attachments of claims
        def _get_attachments(claim):
            return attach_obj.search(
                [('res_model', '=', self._name),
                 ('res_id', '=', claim.id)])

        first_attachments = _get_attachments(base_claim)

        # Counter of all attachments to move.
        # Used to make sure the name is different for all attachments
        existing_names = [att.name for att in first_attachments]
        for claim in self:
            attachments = _get_attachments(claim)
            for attachment in attachments:
                values = {'res_id': base_claim.id}
                name = attachment.name
                count = 1
                while name in existing_names:
                    name = "%s (%s)" % (attachment.name, count)
                    count += 1
                values['name'] = name
                attachment.write(values)
                existing_names.append(name)

    @api.multi
    def _merge_mail_body(self, claim, fields, title=False):
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
                    key = field.selection(self)
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

    @api.multi
    def _merge_notify(self, base_claim):
        """ Create a message gathering merged claims information.  """
        claims = base_claim | self
        # Re-sort claims after union
        claims = claims._merge_sort()

        details = []
        subject = [_('Merged claims')]
        for claim in chain(claims):
            name = claim.name_get()[0][1]
            subject.append(name)
            title = "%s: %s" % (_('Merged claim'), name)
            fields = list(self._merge_fields())
            details.append(self._merge_mail_body(claim, fields, title=title))

        # Chatter message's subject
        subject = subject[0] + ": " + ", ".join(subject[1:])
        details = "\n\n".join(details)
        return base_claim.message_post(body=details, subject=subject)

    @api.multi
    def _merge_followers(self, base_claim):
        """ Subscribe the same followers on the final claim. """
        base_follower_ids = base_claim.sudo().message_follower_ids.ids

        follower_obj = self.env['mail.followers']
        followers = follower_obj.sudo().search(
            [('res_model', '=', self._name),
             ('res_id', 'in', [claim.id for claim in self])]
        )

        for follower in followers:
            if follower.id in base_follower_ids:
                continue
            subtype_ids = [st.id for st in follower.subtype_ids]
            base_claim.sudo().message_subscribe(
                [follower.partner_id.id],
                subtype_ids=subtype_ids
            )

    @api.multi
    def merge(self, base_claim=None):
        """ Merge claims together.

        :param base_claim: the other claims will be merged into this one
            if None, the oldest claim will be selected.
        """

        self._merge_check()
        if base_claim is None:
            base_claim = self._merge_get_default_base()
        # Remove merge_in from self
        self = self.filtered(lambda claim: claim != base_claim)
        # Sort the remaining claims
        self._merge_sort()

        fields = list(self._merge_fields())
        data = self._merge_data(base_claim, fields)

        self._merge_claim_history(base_claim)
        self._merge_claim_attachments(base_claim)

        self._merge_notify(base_claim)
        self._merge_followers(base_claim)

        self._merge_update_foreign_keys(base_claim)
        # Write merged data into first claim
        base_claim.write(data)

        # Delete tail claims
        self.sudo().unlink()

        return base_claim
