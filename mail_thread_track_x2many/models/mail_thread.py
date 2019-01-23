# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models, _


class MailThread(models.Model):
    _inherit = 'mail.thread'

    @api.model
    def _get_tracked_fields(
            self,
            updated_fields,
            suppress_x2many=True):
        result = super(MailThread, self)._get_tracked_fields(
            updated_fields)
        if not result:
            return result
        return dict(filter(
            lambda (y, x): not suppress_x2many
            or x['type'] not in ['one2many', 'many2many'],
            result.iteritems()))

    def _format_value_dict(self, col_info, values_id, values):
        relation_model = self.env[col_info['relation']]
        relation_model_fields = relation_model.fields_get(values.keys())
        message = ''
        for field, value in values.iteritems():
            message += '<br/> ' if message else ''
            message += '%s &rarr; %s' % (
                relation_model_fields[field]['string'], value)
        record_name = ''
        record = relation_model.browse(values_id)
        for (__, name) in record.name_get():
            record_name = name
        return record_name, message

    @api.multi
    def write(self, values):
        x2many_fields = dict(filter(
            lambda (y, x): x['type'] in ['one2many', 'many2many']
            and y in values,
            (self._get_tracked_fields(
                values.keys(),
                suppress_x2many=False) or {}).iteritems()))
        result = super(MailThread, self).write(values)
        if x2many_fields:
            message = '<ul>'
            for field in x2many_fields:
                message += '<li>%s<ul>' % x2many_fields[field].get('string',
                                                                   field)
                for value in values[field]:
                    if value[0] in [3, 4, 5, 6]:
                        continue
                    message += '<li>'
                    if value[0] == 0:
                        message += _('Added: %s') % self._format_value_dict(
                            x2many_fields[field],
                            value[1],
                            value[2])[1]
                    elif value[0] == 1:
                        message += _('Changed %s: %s') % self\
                            ._format_value_dict(
                                x2many_fields[field],
                                value[1],
                                value[2])
                    elif value[0] == 2:
                        message += _('Deleted a line')
                    else:
                        message += '%s' % str(value)
                    message += '</li>'
                message += '</ul></li>'
            message += '</ul>'
            self.message_post(body=message)
        return result
