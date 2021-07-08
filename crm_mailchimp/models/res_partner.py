# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    mailchimp_id = fields.Char(
        help="This is the mailchimp subscriber_id, based on the email address."
    )
    mailchimp_list_ids = fields.Many2many(
        "mailchimp.list", relation="mailchimp_list_res_partner_rel", string="Audiences",
    )
    mailchimp_deleted_list_ids = fields.Many2many(
        "mailchimp.list",
        relation="mailchimp_list_deleted_res_partner_rel",
        string="Deleted audiences",
    )
    mailchimp_interest_ids = fields.Many2many(
        "mailchimp.interest", string="Mailchimp groups"
    )

    def write(self, vals):
        """When removing some list, mark the partner as to be removed from
        said lists. When changing email, keep the old one for syncing new mail
        to mailchimp"""
        lists_per_partner = {}
        if vals.get("mailchimp_list_ids"):
            lists_per_partner = {this: this.mailchimp_list_ids for this in self}
        result = super(ResPartner, self).write(vals)
        if "mailchimp_list_ids" in vals:
            for this, lists in lists_per_partner.items():
                vals = {
                    "mailchimp_deleted_list_ids": [
                        (4, deleted_list.id)
                        for deleted_list in (lists - this.mailchimp_list_ids)
                    ],
                    "mailchimp_interest_ids": [
                        (3, deleted_interest.id)
                        for deleted_interest in (
                            lists - this.mailchimp_list_ids
                        ).mapped("interest_category_ids.interest_ids",)
                    ],
                }
                if not any(vals.values()):
                    continue
                this.write(vals)
        return result
