# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    mailchimp_id = fields.Char(
        help="This is the mailchimp subscriber_id, based on the email address."
    )
    mailchimp_list_ids = fields.Many2many(
        comodel_name="mailchimp.list",
        relation="mailchimp_list_res_partner_rel",
        string="Audiences",
    )
    mailchimp_deleted_list_ids = fields.Many2many(
        comodel_name="mailchimp.list",
        relation="mailchimp_list_deleted_res_partner_rel",
        string="Deleted audiences",
    )
    mailchimp_interest_ids = fields.Many2many(
        comodel_name="mailchimp.interest",
        string="Mailchimp groups",
        domain="[('category_id.list_id', 'in', mailchimp_list_ids)]",
    )

    def write(self, vals):
        """When removing some list, mark the partner as to be removed from
        said lists.
        """
        lists_per_partner = {}
        if vals.get("mailchimp_list_ids"):
            lists_per_partner = {this: this.mailchimp_list_ids for this in self}
        result = super(ResPartner, self).write(vals)
        if "mailchimp_list_ids" in vals:
            for this, lists in lists_per_partner.items():
                # Deleted lists is saved list minus current lists.
                deleted_lists = lists - this.mailchimp_list_ids
                if not deleted_lists:
                    continue
                vals = {
                    # Deleted lists are written used to propagate deletion to mailchimp.
                    # After propagation these records will be removed again.
                    "mailchimp_deleted_list_ids": [
                        (4, deleted_list.id) for deleted_list in deleted_lists
                    ],
                    # Delete the interests linked to the list as well.
                    "mailchimp_interest_ids": [
                        (3, deleted_interest.id)
                        for deleted_interest in deleted_lists.mapped(
                            "interest_category_ids.interest_ids"
                        )
                    ],
                }
                this.write(vals)
        return result
