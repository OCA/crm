# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from werkzeug.exceptions import NotFound

from odoo import exceptions, http
from odoo.http import request


class Mailchimp(http.Controller):
    @http.route(
        "/mailchimp/<string:key>", type="http", auth="none", csrf=False,
    )
    def hook(self, key, **kwargs):
        """Define hook to be called from mailchimp."""
        # mailchimp uses PHP's convention to pass names like data[id], parse
        # this to a dict containing all values
        # if we encounter this kind of thing more often make it a decorator
        args = {}
        for string_path, value in kwargs.items():
            path = [component.rstrip("]") for component in string_path.split("[")]
            current = args
            while path:
                current_name = path.pop(0)
                if path:
                    current.setdefault(current_name, {})
                    current = current[current_name]
                else:
                    current[current_name] = value
        if key != request.env["mailchimp.settings"].sudo()._get_webhook_key():
            raise exceptions.AccessDenied()
        if not args:
            # this is a test request from mailchimp
            return ""
        data = args.get("data", {})
        mailchimp_list = (
            request.env["mailchimp.list"]
            .sudo()
            .search([("mailchimp_id", "=", data.get("list_id"))])
        )
        if not mailchimp_list:
            raise NotFound()
        # Subscriptions are always linked to a specific Audience / List.
        subscriber = (
            request.env["mailchimp.subscriber"]
            .sudo()
            .search(
                [
                    ("list_id", "=", mailchimp_list.id),
                    ("email", "=", data.get("email")),
                ]
            )
        )
        if not subscriber:
            raise NotFound()
        handler = getattr(self, "_hook_%s" % args.get("type"), None)
        if not handler:
            raise NotFound()
        return handler(mailchimp_list, subscriber, data) or ""

    def _hook_unsubscribe(self, mailchimp_list, subscriber, data):
        """Delete subscriber from odoo."""
        if data["action"] in ("unsub", "delete"):
            # We suppose subscriber will have been removed from Mailchimp already.
            subscriber.write({"mailchimp_id": False})
            subscriber.unlink()
