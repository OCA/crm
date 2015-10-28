# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from openerp import models, fields, api


class CrmLead(models.Model):
    """Add third field in lead address"""
    _inherit = "crm.lead"

    street3 = fields.Char('Street 3')

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        return (super(CrmLead, self.with_context(default_street3=lead.street3))
                ._lead_create_contact(lead, name, is_company, parent_id))

    @api.multi
    def on_change_partner_id(self, partner_id):
        res = super(CrmLead, self).on_change_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            res['value'].update({'street3': partner.street3})
        return res
