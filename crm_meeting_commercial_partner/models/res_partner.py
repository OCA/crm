# Author: Jordi Ballester Alomar
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    meeting_count = fields.Integer(
        compute='_compute_meeting_count_commercial_partner')

    @api.multi
    def _compute_meeting_count_commercial_partner(self):
        att_model = self.env['calendar.attendee']
        for partner in self:
            domain = [('partner_id', 'child_of', partner.id)]
            attendees = att_model.read_group(
                domain=domain,
                fields=['event_id'],
                groupby=['event_id']
            )
            partner.meeting_count = len(attendees)

    @api.multi
    def schedule_meeting(self):
        self.ensure_one()
        action = super(ResPartner, self).schedule_meeting()
        action['domain'] = [('partner_ids', 'child_of', self.ids)]
        action['context'].pop('search_default_partner_ids')
        return action
