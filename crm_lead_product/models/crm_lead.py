# Copyright (C) 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    lead_line_ids = fields.One2many(
        comodel_name="crm.lead.line", inverse_name="lead_id", string="Lead Lines"
    )

    @api.onchange("lead_line_ids")
    def _onchange_lead_line_ids(self):
        expected_revenue = 0
        for lead_line in self.lead_line_ids:
            expected_revenue += lead_line.expected_revenue
        self.expected_revenue = expected_revenue

    def _convert_opportunity_data(self, customer, team_id=False):
        res = super()._convert_opportunity_data(customer, team_id)
        expected_revenue = 0
        for lead_line in self.lead_line_ids:
            expected_revenue += lead_line.expected_revenue
        res["expected_revenue"] = expected_revenue
        return res
