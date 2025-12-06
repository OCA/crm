# Copyright 2025 Teacnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models
from odoo.tools import config


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _stage_find(self, team_id=False, domain=None, order="sequence, id", limit=1):
        # adapt the original filtering to support stages with multiple teams
        test_condition = config["test_enable"] and not self.env.context.get(
            "test_crm_stage_multi_team"
        )
        if test_condition or self.env.context.get("no_crm_stage_multi_team"):
            return super()._stage_find(
                team_id=team_id, domain=domain, order=order, limit=limit
            )
        team_ids = set()
        if team_id:
            team_ids.add(team_id)
        for lead in self:
            if lead.team_id:
                team_ids.add(lead.team_id.id)
        # generate the domain
        if team_ids:
            search_domain = [
                "|",
                ("team_ids", "=", False),
                ("team_ids", "in", list(team_ids)),
            ]
        else:
            search_domain = [("team_ids", "=", False)]
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self.env["crm.stage"].search(search_domain, order=order, limit=limit)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        # adapt the method for the field team_ids
        test_condition = config["test_enable"] and not self.env.context.get(
            "test_crm_stage_multi_team"
        )
        if test_condition or self.env.context.get("no_crm_stage_multi_team"):
            return super()._read_group_stage_ids(stages, domain)
        team_ids = self.env.user.crm_team_ids.ids
        if team_ids:
            search_domain = [
                "|",
                ("id", "in", stages.ids),
                "|",
                ("team_ids", "=", False),
                ("team_ids", "in", team_ids),
            ]
        else:
            search_domain = ["|", ("id", "in", stages.ids), ("team_ids", "=", False)]
        # perform search
        stage_ids = stages._search(search_domain, order=stages._order)
        return stages.browse(stage_ids)
