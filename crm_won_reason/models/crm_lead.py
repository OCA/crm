# Copyright 2019 RGB Consulting - Domantas Sidorenkovas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    won_reason = fields.Many2one('crm.won.reason', string='Won Reason',
                                 index=True, track_visibility='onchange')

    @api.multi
    def action_set_won_rainbowman(self):
        self.ensure_one()
        if not self.env.context.get('bypass_won_reason', False):
            action = self.env.ref(
                'crm_won_reason.crm_lead_won_action').read()[0]
            return action
        return super(Lead, self).action_set_won_rainbowman()
