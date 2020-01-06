# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLeadStageProbabilityUpdate(models.TransientModel):

    _name = "crm.lead.stage.probability.update"
    _description = "Mass update of crm lead probability according to stage"

    crm_stage_update_ids = fields.Many2many(
        "crm.lead.stage.probability.update.line",
        "crm_lead_stage_probability_update_line_rel",
        "wizard_id",
        "stage_id",
        readonly=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "crm_stage_update_ids" in fields_list and "active_ids" in self.env.context:
            active_ids = self.env.context.get("active_ids")
            stages = self.env["crm.stage"].browse(active_ids)
            stages_missing_on_change = stages.filtered(lambda s: not s.on_change)
            if stages_missing_on_change:
                raise UserError(
                    _(
                        "Following stages must be set as 'Change Probability "
                        "Automatically' in order to update their related leads:"
                        "\n\n"
                        "%s"
                    )
                    % "\n".join([s.name for s in stages_missing_on_change])
                )
            line_ids = []
            for stage in stages:
                new_line = self.env["crm.lead.stage.probability.update.line"].create(
                    {"stage_id": stage.id}
                )
                line_ids.append(new_line.id)
            res["crm_stage_update_ids"] = [(6, 0, line_ids)]
        return res

    def execute(self):
        updated_leads_ids = []
        for stage_line in self.crm_stage_update_ids:
            leads = self.env["crm.lead"].search(
                [("stage_id", "=", stage_line.stage_id.id)]
            )
            leads.write({"probability": stage_line.stage_id.probability})
            updated_leads_ids += leads.ids
        action = self.env.ref("crm.crm_lead_all_leads").read()[0]
        action["domain"] = "[('id', 'in', %s)]" % updated_leads_ids
        action.pop("context")
        return action


class CrmLeadStageProbabilityUpdateStage(models.TransientModel):

    _name = "crm.lead.stage.probability.update.line"
    _description = "CRM leads stages to updates"

    wizard_id = fields.Many2many(
        "crm.lead.stage.probability.update",
        "crm_lead_stage_probability_update_line_rel",
        "stage_id",
        "wizard_id",
        readonly=True,
    )
    stage_id = fields.Many2one(
        "crm.stage", domain=[("on_change", "=", True)], readonly=True
    )
    lead_count = fields.Integer(
        "No of leads", compute="_compute_lead_count", readonly=True
    )

    @api.depends("stage_id")
    def _compute_lead_count(self):
        for stage_line in self:
            stage_line.lead_count = self.env["crm.lead"].search_count(
                [("stage_id", "=", stage_line.stage_id.id)]
            )
