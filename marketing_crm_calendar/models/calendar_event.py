# Copyright 2025 Juan Alberto Raja <juan.raja@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    campaign_id = fields.Many2one("utm.campaign", "Campaign")
    source_id = fields.Many2one("utm.source", "Source")
    medium_id = fields.Many2one("utm.medium", "Medium")
    phonecall_id = fields.Many2one("crm.phonecall", string="Phonecall", readonly=True)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        if self.env.context.get(
            "active_model"
        ) == "crm.phonecall" and self.env.context.get("active_id"):
            phonecall = self.env["crm.phonecall"].browse(self.env.context["active_id"])
            if phonecall.exists():
                if "phonecall_id" in fields_list:
                    defaults["phonecall_id"] = phonecall.id
                if "campaign_id" in fields_list:
                    defaults["campaign_id"] = phonecall.campaign_id.id
                if "medium_id" in fields_list:
                    defaults["medium_id"] = phonecall.medium_id.id
                if "source_id" in fields_list:
                    defaults["source_id"] = phonecall.source_id.id

        return defaults

    @api.model_create_multi
    def create(self, vals_list):
        events = super().create(vals_list)
        for event, _vals in zip(events, vals_list, strict=False):
            if self.env.context.get(
                "active_model"
            ) == "crm.phonecall" and self.env.context.get("active_id"):
                phonecall_id = self.env.context.get("active_id")
                phonecall = self.env["crm.phonecall"].browse(phonecall_id)
                if phonecall.exists():
                    event.phonecall_id = phonecall_id
                    if phonecall.campaign_id:
                        event.campaign_id = phonecall.campaign_id.id
                    if phonecall.medium_id:
                        event.medium_id = phonecall.medium_id.id
                    if phonecall.source_id:
                        event.source_id = phonecall.source_id.id
        return events
