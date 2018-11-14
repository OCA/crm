# Author: Jordi Ballester Alomar
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    meeting_count = fields.Integer(compute='_compute_meeting_count')

    @api.multi
    def _compute_meeting_count(self):
        super()._compute_meeting_count()
        for partner in self:
            partners = partner + partner.child_ids
            meetings = self.env['calendar.event'].search(
                [('partner_ids', 'in', partners.ids)])
            partner.meeting_count = len(meetings)

    @api.multi
    def schedule_meeting(self):
        self.ensure_one()
        res = super(ResPartner, self).schedule_meeting()
        partners = self + self.child_ids
        res['context']['search_default_partner_ids'] = partners.ids
        return res
