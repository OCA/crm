# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from werkzeug.exceptions import NotFound
from odoo import exceptions, http
from odoo.http import request


class Mailchimp(http.Controller):

    @http.route(
        '/mailchimp/<string:key>', type='http', auth='none', csrf=False,
    )
    # pylint: disable=redefined-builtin
    def hook(self, key, **kwargs):
        # mailchimp uses PHP's convention to pass names like data[id], parse
        # this to a dict containing all values
        # if we encounter this kind of thing more often make it a decorator
        args = {}
        for string_path, value in kwargs.items():
            path = [
                component.rstrip(']') for component in string_path.split('[')
            ]
            current = args
            while path:
                current_name = path.pop(0)
                if path:
                    current.setdefault(current_name, {})
                    current = current[current_name]
                else:
                    current[current_name] = value

        if key != request.env['mailchimp.settings'].sudo()._get_webhook_key():
            raise exceptions.AccessDenied()

        if not args:
            # this is a test request from mailchimp
            return ''

        data = args.get('data', {})

        partner = request.env['res.partner'].sudo().search([
            ('email', '=', data.get('email')),
        ])
        mailchimp_list = request.env['mailchimp.list'].sudo().search([
            ('mailchimp_id', '=', data.get('list_id')),
        ])
        if not partner or not mailchimp_list:
            raise NotFound()

        handler = getattr(self, '_hook_%s' % args.get('type'), None)
        if not handler:
            raise NotFound()

        return handler(mailchimp_list, partner, data) or ''

    def _hook_unsubscribe(self, mailchimp_list, partner, data):
        if data['action'] in ('unsub', 'delete'):
            # we can't just go and delete partners, but we strip them from all
            # mailinglists/interests
            partner.write({
                'mailchimp_list_ids': mailchimp_list.mapped(
                    lambda x: (3, x.id),
                ),
                'mailchimp_interest_ids': mailchimp_list.mapped(
                    'interest_category_ids.interest_ids',
                ).mapped(
                    lambda x: (3, x.id),
                ),
            })
