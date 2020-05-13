# Copyright 2015 Antiun Ingenieria - Endika Iglesias <endikaig@antiun.com>
# Copyright 2017 Tecnativa - Luis Martínez
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.onchange("location_id")
    def on_change_city(self):
        if self.location_id:
            self.update(
                {
                    "zip": self.location_id.name,
                    "city": self.location_id.city_id.name,
                    "state_id": self.location_id.city_id.state_id,
                    "country_id": self.location_id.city_id.country_id,
                }
            )

    location_id = fields.Many2one(
        comodel_name="res.city.zip",
        string="Location",
        index=True,
        help="Use the city name or the zip code to search the location",
    )

    @api.onchange("partner_id")
    def onchange_partner_id_crm_location(self):
        if self.partner_id:
            self.location_id = self.partner_id.zip_id
