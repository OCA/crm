# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    referred_id = fields.Many2one("crm.referred", string="Referred by Categorized")

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(
            partner_name, is_company=is_company, parent_id=parent_id
        )
        res.update(
            {
                "referred_id": self.referred_id.id,
            }
        )
        return res
