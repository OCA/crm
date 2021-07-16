# Copyright 2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MailchimpSubscriberInterest(models.Model):
    """This model links a subscriber to an interest (mailchimp group)."""

    _name = "mailchimp.subscriber.interest"
    _description = "The interests (mailchimp groups) linked to a subscriber."
    _rec_name = "interest_id"  # Only shown from subscribers.

    subscriber_id = fields.Many2one(
        comodel_name="mailchimp.subscriber",
        string="subscriber",
        ondelete="cascade",
        required=True,
    )
    list_id = fields.Many2one(
        comodel_name="mailchimp.list",
        related="subscriber_id.list_id",
        readonly=True,
        required=True,
    )
    interest_id = fields.Many2one(
        comodel_name="mailchimp.interest",
        string="Mailchimp group",
        domain="[('category_id.list_id', '=', list_id)]",
        ondelete="cascade",
        required=True,
    )
