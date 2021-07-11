# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MailchimpMergeField(models.Model):
    _name = "mailchimp.merge.field"
    _description = "Mailchimp merge field"

    name = fields.Char(required=True)
    tag = fields.Char(required=True)
    list_id = fields.Many2one("mailchimp.list", required=True, ondelete="cascade",)
    mailchimp_id = fields.Char(required=True)
    code = fields.Char()

    @api.model
    def _update_from_mailchimp(self, client, mailchimp_list):
        """Create or update merge fields from mailchimp."""
        mail_chimp_merge_fields = client.lists.merge_fields.all(
            get_all=True,
            list_id=mailchimp_list.mailchimp_id,
            fields="merge_fields.name,merge_fields.merge_id," "merge_fields.tag",
        )["merge_fields"]
        for mailchimp_merge_field in mail_chimp_merge_fields:
            merge_field = self.search(
                [
                    ("mailchimp_id", "=", mailchimp_merge_field["merge_id"]),
                    ("list_id", "=", mailchimp_list.id),
                ]
            )
            if merge_field:
                merge_field.write(
                    {
                        "tag": mailchimp_merge_field["tag"],
                        "name": mailchimp_merge_field["name"],
                    }
                )
            else:
                self.create(
                    {
                        "name": mailchimp_merge_field["name"],
                        "list_id": mailchimp_list.id,
                        "mailchimp_id": mailchimp_merge_field["merge_id"],
                        "tag": mailchimp_merge_field["tag"],
                    }
                )
