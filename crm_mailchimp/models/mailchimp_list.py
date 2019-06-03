# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime
import logging
from odoo import api, fields, models, tools
try:
    from mailchimp3 import MailChimp
    from mailchimp3.mailchimpclient import MailChimpError
except ImportError:
    MailChimp = False
    MailChimpError = False


_logger = logging.getLogger(__name__)


class MailchimpList(models.Model):
    _name = 'mailchimp.list'
    _description = 'A mailchimp audience'

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    mailchimp_id = fields.Char(required=True)
    interest_category_ids = fields.One2many(
        'mailchimp.interest.category', 'list_id',
        string='Groups',
    )
    merge_field_ids = fields.One2many(
        'mailchimp.merge.field', 'list_id',
        string='Merge fields',
    )
    group_ids = fields.Many2many('res.groups', help='Restricted to groups')

    @api.model
    @tools.ormcache()
    def _get_mailchimp_client(self):
        return MailChimp(
            mc_api=self.env['ir.config_parameter'].get_param(
                'crm_mailchimp.apikey'
            ),
            mc_user=self.env['ir.config_parameter'].get_param(
                'crm_mailchimp.username'
            ),
        )

    @api.model
    def _read_from_mailchimp(self):
        client = self._get_mailchimp_client()
        for mailchimp_list in client.lists.all(
                get_all=True, fields='lists.name,lists.id'
        )['lists']:
            this = self.search([
                ('mailchimp_id', '=', mailchimp_list['id'])
            ]) or self.create({
                'name': mailchimp_list['name'],
                'mailchimp_id': mailchimp_list['id'],
            })
            this._update_from_mailchimp()

    @api.multi
    def _update_from_mailchimp(self):
        client = self._get_mailchimp_client()
        for this in self:
            mailchimp_list = client.lists.get(this.mailchimp_id)
            this.write({'name': mailchimp_list['name']})
            for mailchimp_merge_field in client.lists.merge_fields.all(
                    get_all=True, list_id=this.mailchimp_id,
                    fields='merge_fields.name,merge_fields.merge_id,'
                    'merge_fields.tag',
            )['merge_fields']:
                merge_field = self.env['mailchimp.merge.field'].search([
                    ('mailchimp_id', '=', mailchimp_merge_field['merge_id']),
                    ('list_id', '=', this.id),
                ]) or self.env['mailchimp.merge.field'].create({
                    'name': mailchimp_merge_field['name'],
                    'list_id': this.id,
                    'mailchimp_id': mailchimp_merge_field['merge_id'],
                    'tag': mailchimp_merge_field['tag'],
                })
                merge_field._update_from_mailchimp()
            for mailchimp_category in client.lists.interest_categories.all(
                    get_all=True, list_id=this.mailchimp_id,
                    fields='categories.title,categories.id',
            )['categories']:
                category = self.env['mailchimp.interest.category'].search([
                    ('mailchimp_id', '=', mailchimp_category['id']),
                    ('list_id', '=', this.id),
                ]) or self.env['mailchimp.interest.category'].create({
                    'name': mailchimp_category['title'],
                    'list_id': this.id,
                    'mailchimp_id': mailchimp_category['id'],
                })
                category._update_from_mailchimp()

    @api.multi
    def _push_to_mailchimp(self, modified_after=None):
        date_domain = []
        if modified_after:
            date_domain = [('write_date', '>=', modified_after)]
        for this in self:
            for partner in self.env['res.partner'].search(date_domain + [
                    ('mailchimp_list_ids', 'in', this.ids),
                    ('email', '!=', False),
            ]):
                try:
                    this._push_partner_to_mailchimp(partner)
                except MailChimpError:
                    _logger.exception(
                        'Error pushing partner %d to mailchimp', partner,
                    )
                # reset a possibly changed email address, see res.parter#write
                partner.write({
                    'mailchimp_last_email': False,
                })

            for partner in self.env['res.partner'].search(date_domain + [
                    ('mailchimp_deleted_list_ids', 'in', this.ids),
                    ('email', '!=', False),
            ]):
                try:
                    this._remove_partner_from_mailchimp(partner)
                except MailChimpError:
                    _logger.exception(
                        'Error pushing partner %d to mailchimp', partner,
                    )
                partner.write({'mailchimp_deleted_list_ids': [(3, this.id)]})

    @api.multi
    def _remove_partner_from_mailchimp(self, partner):
        self.ensure_one()
        client = self._get_mailchimp_client()
        client.lists.members.delete(
            list_id=self.mailchimp_id,
            subscriber_hash=partner.mailchimp_id,
        )

    @api.multi
    def _push_partner_to_mailchimp(self, partner):
        self.ensure_one()
        client = self._get_mailchimp_client()
        client.lists.members.create_or_update(
            list_id=self.mailchimp_id,
            subscriber_hash=partner.mailchimp_id,
            data=self._push_partner_to_mailchimp_data(partner),
        )

    @api.multi
    def _push_partner_to_mailchimp_data(self, partner):
        self.ensure_one()
        data = {
            'email_address': partner.email,
            'status': 'subscribed',
            'status_if_new': 'subscribed',
            'merge_fields': {
                merge_field.tag: tools.safe_eval.safe_eval(
                    merge_field.code, {'partner': partner}, mode='eval'
                )
                for merge_field in self.merge_field_ids
                if merge_field.code
            },
            'interests': {
                interest.mailchimp_id: bool(
                    partner.mailchimp_interest_ids & interest
                )
                for interest in
                self.mapped('interest_category_ids.interest_ids')
            }
        }
        return data

    @api.multi
    def action_update(self):
        return self._update_from_mailchimp()

    @api.multi
    def action_push(self):
        return self._push_to_mailchimp()

    @api.model
    def _cron(self, lookbehind=None):
        modified_after = None
        if lookbehind:
            modified_after = fields.Datetime.to_string(
                datetime.datetime.now() - datetime.timedelta(
                    seconds=lookbehind,
                )
            )
        self.search([])._push_to_mailchimp(modified_after=modified_after)
