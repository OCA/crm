# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MailchimpInterestCategory(models.Model):
    _name = 'mailchimp.interest.category'
    _description = 'Mailchimp group'

    name = fields.Char(required=True)
    list_id = fields.Many2one(
        'mailchimp.list', required=True, ondelete='cascade',
    )
    mailchimp_id = fields.Char(required=True)
    interest_ids = fields.One2many(
        'mailchimp.interest', 'category_id', string='Mailchimp groups',
    )
    group_ids = fields.Many2many(
        'res.groups', string='Odoo groups', help='Restricted to groups',
    )

    @api.multi
    def _update_from_mailchimp(self):
        client = self.env['mailchimp.list']._get_mailchimp_client()
        for this in self:
            for mc_interest in client.lists.interest_categories.interests.all(
                    get_all=True,
                    list_id=this.list_id.mailchimp_id,
                    category_id=this.mailchimp_id,
                    fields='interests.name,interests.id',
            )['interests']:
                interest = self.env['mailchimp.interest'].search([
                    ('category_id', '=', this.id),
                    ('mailchimp_id', '=', mc_interest['id']),
                ]) or self.env['mailchimp.interest'].create({
                    'name': mc_interest['name'],
                    'category_id': this.id,
                    'mailchimp_id': mc_interest['id'],
                })
                interest._update_from_mailchimp()
