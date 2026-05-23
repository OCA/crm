# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    interest_group_ids = fields.Many2many(
        comodel_name="res.partner.interest.group",
        string="Interest Groups",
    )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        values = super()._prepare_customer_values(
            partner_name, is_company=is_company, parent_id=parent_id
        )
        if self.interest_group_ids:
            values["interest_group_ids"] = [(6, 0, self.interest_group_ids.ids)]
        return values
