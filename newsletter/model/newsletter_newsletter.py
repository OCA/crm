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
from openerp import api, models, fields, exceptions, _
from openerp.tools.safe_eval import safe_eval
_logger = logging.getLogger(__name__)


class newsletter_newsletter(models.Model):
    _name = 'newsletter.newsletter'
    _description = 'Newsletter'
    _rec_name = 'subject'
    _order = 'create_date desc'
    _logger = logging.getLogger(_name)

    _state_selection = [
        ('draft', 'Draft'),
        ('testing', 'Testing'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
    ]

    def _may_send_get(self):
        for this in self:
            user_groups = set(group.id for group in self.env.user.groups_id)
            result = True
            if this.type_id.group_ids:
                result = bool(user_groups.intersection(
                    set(group.id for group in this.type_id.group_ids)))
            this['may_send'] = result

    state = fields.Selection(
        _state_selection, 'State', default='draft', required=True)
    type_id = fields.Many2one('newsletter.type', 'Type', required=True)
    subject = fields.Char('Subject', required=True)
    text_intro_html = fields.Text('Intro')
    text_outro_html = fields.Text('Outro')
    topic_ids = fields.One2many('newsletter.topic', 'newsletter_id', 'Topics')
    may_send = fields.Boolean('May send', compute=_may_send_get)

    @api.multi
    def action_preview(self):
        if self.state not in ['testing', 'sending', 'sent']:
                self.write({'state': 'testing'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'email_template.preview',
            'target': 'new',
            'context': {
                'template_id': self.type_id.email_template_id.id,
                'default_res_id': self.id,
                'newsletter_res_id': self.env[self.type_id.model.model].search(
                    safe_eval(self.type_id.domain)).ids[-1:] or False,
            },
            'view_mode': 'form',
            'view_id': self.env.ref(
                'newsletter.email_template_preview_form').id,
        }

    @api.multi
    def action_send(self):
        self.write({'state': 'sending'})
        self.env['ir.cron'].sudo().create({
            'name': 'newsletter._cronjob_send_newsletter',
            'user_id': self.env.uid,
            'priority': 9,
            'model': self._model._name,
            'function': '_cronjob_send_newsletter',
            'args': str((self.ids,)),
            'interval_type': False,
            'numbercall': 1,
            'doall': False,
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.one
    def _cronjob_send_newsletter(self):
        model = self.env[self.type_id.model.model]

        step = 100
        offset = 0
        search_domain = safe_eval(self.type_id.domain)

        _logger.info('sending newsletter %s', self.subject)
        _logger.debug(
            'searching for %s %s', self.type_id.model.model, search_domain)

        while True:
            records = model.search(search_domain, offset=offset, limit=step)
            if not records:
                break
            for record in records:
                try:
                    self._do_send_newsletter(record)
                except Exception as e:
                    _logger.error(e)
            offset += step
        _logger.info('sending newsletter %s finished', self.subject)
        self.write({'state': 'sent'})

    @api.one
    def _do_send_newsletter(self, record, context=None):
        _logger.debug('sending mail to %d', record)
        self.type_id.email_template_id\
            .with_context(
                newsletter_res_id=record.id)\
            .send_mail(self.id)

    @api.multi
    def action_show_recipient_objects(self):
        return self.type_id.action_show_recipient_objects()

    @api.multi
    def unlink(self):
        for this in self:
            if this.state in ['sending', 'sent']:
                raise exceptions.ValidationError(
                    _('You can\'t delete sent newsletters!'))
        return super(newsletter_newsletter, self).unlink()
