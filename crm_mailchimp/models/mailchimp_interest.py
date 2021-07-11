# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MailchimpInterest(models.Model):
    _name = "mailchimp.interest"
    _order = "category_id, name"
    _description = "Mailchimp group"

    name = fields.Char(required=True)
    category_id = fields.Many2one(
        "mailchimp.interest.category", required=True, ondelete="cascade",
    )
    mailchimp_id = fields.Char(required=True)

    @api.model
    def _update_from_mailchimp(self, client, category):
        """Update interests for category from mailchimp."""
        interests = client.lists.interest_categories.interests.all(
            get_all=True,
            list_id=category.list_id.mailchimp_id,
            category_id=category.mailchimp_id,
            fields="interests.name,interests.id",
        )["interests"]
        for mc_interest in interests:
            interest = self.search(
                [
                    ("category_id", "=", category.id),
                    ("mailchimp_id", "=", mc_interest["id"]),
                ]
            )
            if interest:
                interest.write({"name": mc_interest["name"]})
            else:
                self.create(
                    {
                        "name": mc_interest["name"],
                        "category_id": category.id,
                        "mailchimp_id": mc_interest["id"],
                    }
                )

    def name_get(self):
        return [
            (this.id, "{}: {}".format(this.category_id.name, this.name))
            for this in self
        ]
