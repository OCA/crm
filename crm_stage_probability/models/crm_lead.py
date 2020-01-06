# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, tools


class CrmLead(models.Model):

    _inherit = "crm.lead"

    def _default_probability(self):
        if "default_stage_id" in self._context:
            stage_id = self._context.get("default_stage_id")
        else:
            stage_id = self._default_stage_id()
        if stage_id:
            return self.env["crm.stage"].browse(stage_id).probability
        return 10

    is_stage_probability = fields.Boolean(
        compute="_compute_is_stage_probability", readonly=True
    )
    stage_probability = fields.Float(related="stage_id.probability", readonly=True)
    probability = fields.Float(default=lambda self: self._default_probability())

    @api.depends("probability", "stage_id", "stage_id.probability")
    def _compute_is_stage_probability(self):
        for lead in self:
            lead.is_stage_probability = (
                tools.float_compare(lead.probability, lead.stage_probability, 2) == 0
            )

    @api.depends("probability", "automated_probability")
    def _compute_is_automated_probability(self):
        for lead in self:
            if lead.probability != lead.stage_id.probability:
                super(CrmLead, lead)._compute_is_automated_probability()
                continue
            lead.is_automated_probability = False

    def _update_probability(self):
        self = self.with_context(_auto_update_probability=True)
        return super()._update_probability()

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        if not stage_id:
            return {}
        stage = self.env["crm.stage"].browse(stage_id)
        if stage.on_change:
            return {"probability": stage.probability}
        return {}

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        res = super()._onchange_stage_id()
        values = self._onchange_stage_id_values(self.stage_id.id)
        self.update(values)
        return res

    def write(self, vals):
        # Avoid to update probability with automated_probability on
        # _update_probability if the stage is set as on_change
        # If the stage is not set as on_change, auto PLS will be applied
        if (
            self.env.context.get("_auto_update_probability")
            and "probability" in vals
            and "stage_id" not in vals
        ):
            vals.update(self._onchange_stage_id_values(self.stage_id.id))
        # Force to use the probability from the stage if set as on_change
        if vals.get("stage_id") and "probability" not in vals:
            vals.update(self._onchange_stage_id_values(vals.get("stage_id")))
        return super().write(vals)

    def action_set_stage_probability(self):
        self.write({"probability": self.stage_id.probability})
