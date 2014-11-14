# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
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

import logging
from openerp.osv.orm import Model, except_orm
from openerp.osv import fields
from openerp.tools.safe_eval import safe_eval
from .newsletter_type import newsletter_type
from openerp.tools.translate import _


def _get_plaintext(obj, cr, uid, ids, field_name, arg, context=None):
    # TODO: we need a write function for that too
    result = {}
    for this in obj.browse(cr, uid, ids, context=context):
        if this.plaintext_mode == 'from_html' and this[arg]:
            from lxml import html

            doc = html.document_fromstring(this[arg])
            result[this.id] = doc.text_content()
        else:
            # TODO: read from database
            result[this.id] = ''
    return result


class newsletter_newsletter(Model):
    _name = 'newsletter.newsletter'
    _description = 'Newsletter'
    _rec_name = 'subject'
    _logger = logging.getLogger(_name)

    _state_selection = [
        ('draft', 'draft'),
        ('testing', 'testing'),
        ('sending', 'sending'),
        ('sent', 'sent'),
    ]

    def _may_send_get(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        user_groups = set([
            group.id for group in
            self.pool.get('res.users').browse(
                cr, uid, uid, context=context).groups_id
        ])

        for this in self.browse(cr, uid, ids, context=context):
            result[this.id] = True
            if this.type_id.group_ids:
                result[this.id] = bool(user_groups.intersection(
                    set([group.id for group in this.type_id.group_ids])))

        return result

    _columns = {
        'state': fields.selection(_state_selection, 'State'),
        'type_id': fields.many2one(
            'newsletter.type', 'Type', required=True),
        'subject': fields.char('Subject', size=256, required=True),
        'text_intro_plain': fields.function(
            _get_plaintext, type='text', string='Intro (plain)',
            arg='text_intro_html', store=True),
        'text_intro_html': fields.text('Intro (HTML)'),
        'text_outro_plain': fields.function(
            _get_plaintext, type='text', string='Outro (plain)',
            arg='text_outro_html', store=True),
        'text_outro_html': fields.text('Outro (HTML)'),
        'topic_ids': fields.one2many(
            'newsletter.topic', 'newsletter_id', 'Topics'),
        'plaintext_mode': fields.related(
            'type_id', 'plaintext_mode', type='selection',
            selection=newsletter_type._plaintext_mode_selection,
            string='Plaintext mode', readonly=True),
        'may_send': fields.function(_may_send_get, type='boolean'),
    }

    _defaults = {
        'state': 'draft',
    }

    def on_change_type_id(self, cr, uid, ids, type_id, context=None):
        newsletter_type = self.pool.get('newsletter.type').browse(
            cr, uid, type_id, context=context)
        return {
            'value': {
                'plaintext_mode': newsletter_type.plaintext_mode,
            }
        }

    def action_preview(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context):
            if this.state not in ['testing', 'sending', 'sent']:
                this.write({'state': 'testing'})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'email_template.preview',
                'target': 'new',
                'context': {
                    'template_id': this.type_id.email_template_id.id,
                    'default_res_id': this.id,
                    'newsletter_res_id':
                        self.pool[this.type_id.model.model].search(
                            cr, uid, safe_eval(this.type_id.domain))[0],
                },
                'view_mode': 'form',
                'view_id': self.pool.get('ir.model.data').get_object_reference(
                    cr, uid, 'newsletter', 'email_template_preview_form')[1],
            }

    def action_send(self,  cr,  uid,  ids,  context=None):
        self.write(cr, uid, ids, {'state': 'sending'}, context=context)
        self.pool.get('ir.cron').create(
            cr, uid,
            {
                'name': 'newsletter._cronjob_send_newsletter',
                'user_id': uid,
                'priority': 9,
                'model': self._name,
                'function': '_cronjob_send_newsletter',
                'args': str((ids,)),
                'interval_type': False,
                'numbercall': 1,
                'doall': False,
            })
        return {'type': 'ir.actions.act_window_close'}

    def _cronjob_send_newsletter(self,  cr,  uid,  ids,  context=None):
        for this in self.browse(cr,  uid,  ids,  context):
            model = self.pool.get(this.type_id.model.model)

            step = 100
            offset = 0
            search_domain = safe_eval(this.type_id.domain)

            self._logger.info('sending newsletter %s' % this.subject)
            self._logger.debug('searching for %s %s' % (
                this.type_id.model.model, search_domain))

            while True:
                ids = model.search(
                    cr, uid, search_domain, offset=offset, limit=step)

                if not ids:
                    break

                for id in ids:
                    try:
                        self._do_send_newsletter(cr, uid, this, id,
                                                 context=context)
                    except Exception as e:
                        self._logger.error(e)

                offset += step

            self._logger.info('sending newsletter %s finished' % this.subject)
            this.write({'state': 'sent'})

    def _do_send_newsletter(self, cr, uid, this, record_id, context=None):
        self._logger.debug('sending mail to %d' % record_id)
        self.pool['email.template'].send_mail(
            cr,
            uid,
            this.type_id.email_template_id.id,
            this.id,
            context={
                'newsletter_res_id': record_id
            })

    def action_show_recipient_objects(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            return this.type_id.action_show_recipient_objects()

    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            if this.state in ['sending', 'sent']:
                raise except_orm(_('Error'),
                                 _('You can\'t delete sent newsletters!'))
        return super(newsletter_newsletter, self).unlink(cr, uid, ids,
                                                         context=context)
