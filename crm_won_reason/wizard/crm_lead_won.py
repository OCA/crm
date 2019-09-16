# Copyright 2019 RGB Consulting - Domantas Sidorenkovas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLeadWon(models.TransientModel):
    _name = 'crm.lead.won'
    _description = 'Get Won Reason'

    won_reason_id = fields.Many2one('crm.won.reason', 'Won Reason')

    @api.multi
    def action_won_reason_apply(self):
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        leads.write({'won_reason': self.won_reason_id.id})
        return leads.with_context(
            bypass_won_reason=True).action_set_won_rainbowman()
