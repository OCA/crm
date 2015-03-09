# -*- coding: utf-8 -*-
#
#
#    Author: Romain Deheele
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields, api


class CrmLeadLost(models.TransientModel):

    """ Ask a reason for the opportunity lost."""
    _name = 'crm.lead.lost'
    _description = __doc__

    def _default_reason(self):
        active_id = self._context.get('active_id')
        active_model = self._context.get('active_model')
        if active_id and active_model == 'crm.lead':
            lead = self.env['crm.lead'].browse(active_id)
            return lead.lost_reason_id.id

    reason_id = fields.Many2one(
        'crm.lead.lost.reason',
        string='Reason',
        required=True,
        default=_default_reason)

    @api.one
    def confirm_lost(self):
        act_close = {'type': 'ir.actions.act_window_close'}
        lead_ids = self._context.get('active_ids')
        if lead_ids is None:
            return act_close
        assert len(lead_ids) == 1, "Only 1 lead ID expected"
        lead = self.env['crm.lead'].browse(lead_ids)
        lead.lost_reason_id = self.reason_id.id
        lead.case_mark_lost()
        return act_close
