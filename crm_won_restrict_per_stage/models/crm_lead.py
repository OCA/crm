# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CrmStage(models.Model):
    _inherit = "crm.lead"

    show_won_button = fields.Boolean(related="stage_id.show_won_button")

    def write(self, vals):
        for rec in self:
            if vals.get("stage_id"):
                stage = self.env["crm.stage"].browse(vals.get("stage_id"))
                if stage.is_won and not rec.stage_id.show_won_button:
                    raise ValidationError(
                        _("You can't change to this stage from the current stage.")
                    )
        return super().write(vals)
