# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria - Endika Iglesias <endikaig@antiun.com>
# Copyright 2017 Tecnativa - Luis Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
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

    @api.onchange('partner_id')
    def onchange_partner_id_crm_location(self):
        if self.partner_id:
            self.location_id = self.partner_id.zip_id.id
