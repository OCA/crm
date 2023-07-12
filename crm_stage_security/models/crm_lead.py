# Copyright 2023 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import _, api, models
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.constrains("stage_id")
    def _check_stage(self):
        for rec in self:
            groups = rec.stage_id.group_ids
            if not groups:
                continue
            user_groups = self.env.user.groups_id
            if any(user_group in groups for user_group in user_groups):
                continue
            raise ValidationError(
                _(
                    "You are not allowed to move a lead to this stage\nThe only "
                    "allowed groups are:\n%(groups)s",
                    groups="\n".join(groups.mapped("name")),
                )
            )
