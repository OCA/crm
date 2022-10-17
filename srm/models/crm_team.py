# Copyright 2022 Telmo Santos <telmo.santos@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Team(models.Model):
    _inherit = "crm.team"

    @api.model
    def action_your_pipeline(self):
        action = super().action_your_pipeline()
        request_type = self.env.context.get("request_type")
        if request_type:
            action[
                "domain"
            ] = "[('type','=','opportunity'), ('request_type', '=', '{}')]".format(
                request_type
            )
            action["context"]["default_request_type"] = request_type
        return action
