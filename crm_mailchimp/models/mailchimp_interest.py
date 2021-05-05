# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MailchimpInterest(models.Model):
    _name = "mailchimp.interest"
    _order = "category_id, name"
    _description = "Mailchimp group"

    name = fields.Char(required=True)
    category_id = fields.Many2one(
        "mailchimp.interest.category", required=True, ondelete="cascade",
    )
    mailchimp_id = fields.Char(required=True)

    def _update_from_mailchimp(self):
        pass

    def name_get(self):
        return [
            (this.id, "{}: {}".format(this.category_id.name, this.name))
            for this in self
        ]
