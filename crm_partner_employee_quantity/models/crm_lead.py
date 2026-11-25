# Copyright 2026 Binhex -  Adasat Torres de León
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    employee_quantity = fields.Integer()
    employee_quantity_range_id = fields.Many2one(
        comodel_name="res.partner.employee_quantity_range",
        string="Employee quantity range",
    )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(partner_name, is_company, parent_id)
        if is_company:
            res.update(
                {
                    "employee_quantity": self.employee_quantity,
                    "employee_quantity_range_id": self.employee_quantity_range_id.id,
                }
            )
        return res
