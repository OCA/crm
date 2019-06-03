# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MailchimpMergeField(models.Model):
    _name = 'mailchimp.merge.field'
    _description = 'Mailchimp merge field'

    name = fields.Char(required=True)
    tag = fields.Char(required=True)
    list_id = fields.Many2one(
        'mailchimp.list', required=True, ondelete='cascade',
    )
    mailchimp_id = fields.Char(required=True)
    code = fields.Char(default="'/'")

    @api.multi
    def _update_from_mailchimp(self):
        client = self.env['mailchimp.list']._get_mailchimp_client()
        for this in self:
            merge_field_data = client.lists.merge_fields.get(
                list_id=this.list_id.mailchimp_id, merge_id=this.mailchimp_id,
            )
            this.write({
                'tag': merge_field_data['tag'],
                'name': merge_field_data['name'],
            })
