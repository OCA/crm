# -*- encoding: utf-8 -*-
# Author: Jordi Ballester Alomar
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.osv import orm, fields as old_fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def schedule_meeting(self):
        self.ensure_one()
        res = super(ResPartner, self).schedule_meeting()
        partners = self + self.child_ids
        res['context']['search_default_partner_ids'] = partners.ids
        return res


# To refactor in v10
class ResPartnerOrm(orm.Model):
    _inherit = 'res.partner'

    def _opportunity_meeting_count(self, cr, uid, ids, field_name, arg,
                                   context=None):
        res = super(ResPartnerOrm, self)._opportunity_meeting_count(
            cr, uid, ids, field_name, arg, context=context)
        for partner in self.browse(cr, uid, ids, context):
            if partner.is_company:
                operator = 'child_of'
            else:
                operator = 'in'
            meeting_ids = self.pool['calendar.event'].search(
                cr, uid, [('partner_ids', operator, [partner.id])],
                context=context)
            res[partner.id]['meeting_count'] = len(meeting_ids)
        return res

    _columns = {
        'opportunity_count': old_fields.function(
            _opportunity_meeting_count, string="Opportunity",
            type='integer', multi='opp_meet'),
        'meeting_count': old_fields.function(
            _opportunity_meeting_count,
            string="# Meetings", type='integer', multi='opp_meet'),
    }
