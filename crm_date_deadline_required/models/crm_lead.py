from odoo import _, api, models
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.constrains("date_deadline", "type")
    def _check_date_deadline_required(self):
        for record in self:
            if record.type == "opportunity" and not record.date_deadline:
                raise ValidationError(
                    _("The expected closing date is required for opportunities.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("type") == "opportunity" and not vals.get("date_deadline"):
                raise ValidationError(
                    _("The expected closing date is required for opportunities.")
                )
        return super().create(vals_list)
