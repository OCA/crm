# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MailchimpInterestCategory(models.Model):
    _name = "mailchimp.interest.category"
    _description = "Mailchimp group"

    name = fields.Char(required=True)
    list_id = fields.Many2one("mailchimp.list", required=True, ondelete="cascade",)
    interest_ids = fields.One2many(
        comodel_name="mailchimp.interest",
        inverse_name="category_id",
        string="Mailchimp groups",
    )
    group_ids = fields.Many2many(
        comodel_name="res.groups", string="Odoo groups", help="Restricted to groups",
    )
    mailchimp_id = fields.Char(required=True)

    @api.model
    def _update_from_mailchimp(self, client, mailchimp_list):
        """Update interest categories and underlying interests from mailchimp."""
        interest_model = self.env["mailchimp.interest"]
        mailchimp_categories = client.lists.interest_categories.all(
            get_all=True,
            list_id=mailchimp_list.mailchimp_id,
            fields="categories.title,categories.id",
        )["categories"]
        for mailchimp_category in mailchimp_categories:
            category = self.env["mailchimp.interest.category"].search(
                [
                    ("mailchimp_id", "=", mailchimp_category["id"]),
                    ("list_id", "=", mailchimp_list.id),
                ]
            )
            if category:
                category.write({"name": mailchimp_category["title"]})
            else:
                category = self.create(
                    {
                        "name": mailchimp_category["title"],
                        "list_id": mailchimp_list.id,
                        "mailchimp_id": mailchimp_category["id"],
                    }
                )
            interest_model._update_from_mailchimp(client, category)
