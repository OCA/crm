# Copyright 2015 Antiun Ingenieria - Endika Iglesias <endikaig@antiun.com>
# Copyright 2017 Tecnativa - Luis Martínez
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    location_id = fields.Many2one(
        comodel_name="res.city.zip",
        string="Location",
        index="btree",
        help="Use the city name or the zip code to search the location",
        compute="_compute_location_id",
        readonly=False,
        store=True,
    )

    @api.depends("location_id")
    def _compute_partner_address_values(self):
        res = super()._compute_partner_address_values()
        for lead in self.filtered("location_id"):
            lead.update(
                {
                    "zip": lead.location_id.name,
                    "city": lead.location_id.city_id.name,
                    "state_id": lead.location_id.city_id.state_id,
                    "country_id": lead.location_id.city_id.country_id,
                }
            )
        return res

    @api.depends("partner_id")
    def _compute_location_id(self):
        for lead in self:
            if lead.partner_id.zip_id:
                lead.location_id = lead.partner_id.zip_id.id
            elif lead.location_id:
                lead.location_id = lead.location_id.id
