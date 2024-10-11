# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    role_ids = fields.Many2many(
        comodel_name="res.partner.role",
        compute="_compute_role_ids",
        readonly=False,
        store=True,
        string="Roles",
    )

    @api.depends("partner_id")
    def _compute_role_ids(self):
        for lead in self:
            lead.role_ids = lead.partner_id.role_ids

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        vals = super()._prepare_customer_values(partner_name, is_company, parent_id)
        if self.role_ids:
            vals["role_ids"] = self.role_ids
        return vals
