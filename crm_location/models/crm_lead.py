# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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
    _inherit = 'crm.lead'

    @api.one
    @api.onchange('location_id')
    def on_change_city(self):
        if self.location_id:
            self.zip = self.location_id.name
            self.city = self.location_id.city
            self.state_id = self.location_id.state_id
            self.country_id = self.location_id.country_id

    location_id = fields.Many2one(
        'res.better.zip',
        string='Location',
        index=True,
        help='Use the city name or the zip code to search the location',
    )

    @api.multi
    def on_change_partner_id(self, partner_id):
        res = super(CrmLead, self).on_change_partner_id(partner_id)
        if 'value' not in res:
            res['value'] = {}
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            res['value']['location_id'] = partner.zip_id.id
        return {'value': res['value']}
