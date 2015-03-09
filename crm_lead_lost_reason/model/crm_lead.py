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

from openerp import models, fields, api, exceptions


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lost_reason_id = fields.Many2one(
        'crm.lead.lost.reason',
        string="Reason for lost",
        readonly=True,
        ondelete="restrict")

    @api.multi
    def write(self, vals):
        """Check if a lost reason is given when you
        mark an opportunity as lost.
        If there is no lost reason, it indicates you to pass by form
        to provide a lost reason. It's the choice of the simplicity to
        avoid to struggle with kanban javascript code.
        Erases too the lost reason if the lead is passed from lost to
        another stage.
        """
        if 'stage_id' in vals:
            new_stage = self.env['crm.case.stage'].browse(vals['stage_id'])
            lost_stage = self.env.ref('crm.stage_lead7')
            for lead in self:
                if new_stage == lost_stage and not lead.lost_reason_id:
                    raise exceptions.Warning('Please pass by the red button '
                                             '"Mark Lost" on the form '
                                             'to provide a lost reason.')
                if lead.stage_id == lost_stage and new_stage != lost_stage:
                    lead.lost_reason_id = False
        result = super(CrmLead, self).write(vals)
        return result


class CrmLeadLostReason(models.Model):
    _name = 'crm.lead.lost.reason'
    _description = 'Crm Lead Lost Reason'

    name = fields.Char('Reason', required=True, translate=True)
