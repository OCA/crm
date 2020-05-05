##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    code = fields.Char(
        string="Lead Number", required=True, default="/", readonly=True, copy=False
    )

    _sql_constraints = [
        ("crm_lead_unique_code", "UNIQUE (code)", _("The code must be unique!")),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "/") == "/":
                vals["code"] = self.env.ref(
                    "crm_lead_code.sequence_lead", raise_if_not_found=False
                ).next_by_id()
        return super().create(vals_list)
