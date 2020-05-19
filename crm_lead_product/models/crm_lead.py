# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_line_ids = fields.One2many(
        comodel_name='crm.lead.line',
        inverse_name='lead_id',
        string='Lead Lines',
    )

    @api.onchange('lead_line_ids')
    def _onchange_lead_line_ids(self):
        planned_revenue = 0
        for lead_line in self.lead_line_ids:
            if lead_line.planned_revenue != 0:
                planned_revenue += lead_line.planned_revenue
                self.planned_revenue = planned_revenue

    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
        res = super(CrmLead, self)._convert_opportunity_data(customer, team_id)

        # Update planned_revenue
        planned_revenue = 0
        for lead_line in self.lead_line_ids:
            planned_revenue += lead_line.planned_revenue

        res['planned_revenue'] = planned_revenue

        return res
