# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import hashlib
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    mailchimp_id = fields.Char(compute='_compute_mailchimp_id')
    mailchimp_list_ids = fields.Many2many(
        'mailchimp.list', relation='mailchimp_list_res_partner_rel',
        string='Audiences',
    )
    mailchimp_deleted_list_ids = fields.Many2many(
        'mailchimp.list', relation='mailchimp_list_deleted_res_partner_rel',
        string='Deleted audiences',
    )
    mailchimp_last_email = fields.Char()
    mailchimp_interest_ids = fields.Many2many(
        'mailchimp.interest', string='Groups',
    )

    @api.multi
    def _compute_mailchimp_id(self):
        for this in self:
            this.mailchimp_id = hashlib.md5(
                (this.mailchimp_last_email or this.email or '').lower()
            ).hexdigest()

    @api.multi
    def write(self, vals):
        """When removing some list, mark the partner as to be removed from
        said lists. When changing email, keep the old one for syncing new mail
        to mailchimp"""
        lists_per_partner = {}
        if vals.get('mailchimp_list_ids'):
            lists_per_partner = {
                this: this.mailchimp_list_ids
                for this in self
            }
        if 'email' in vals:
            emails_per_partner = {
                this: this.email
                for this in self
            }
        result = super(ResPartner, self).write(vals)
        if 'mailchimp_list_ids' in vals:
            for this, lists in lists_per_partner.items():
                vals = {
                    'mailchimp_deleted_list_ids': [
                        (4, deleted_list.id)
                        for deleted_list in
                        (lists - this.mailchimp_list_ids)
                    ],
                    'mailchimp_interest_ids': [
                        (3, deleted_interest.id)
                        for deleted_interest in
                        (lists - this.mailchimp_list_ids).mapped(
                            'interest_category_ids.interest_ids',
                        )
                    ],
                }
                if not any(vals.values()):
                    continue
                this.write(vals)
        if 'email' in vals:
            for this, email in emails_per_partner.items():
                this.write({
                    # as this field is reset when syncing, keep the first
                    # changed addres since last sync, because this is what
                    # mailchimp knows
                    'mailchimp_last_email': this.mailchimp_last_email or email,
                })
        return result
