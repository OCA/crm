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
                seq_date = fields.Date.context_today(self)
                vals["code"] = (
                    self.env["ir.sequence"]
                    .with_company(self.company_id)
                    .next_by_code("crm.lead", sequence_date=seq_date)
                )
        return super(CrmLead, self).create(vals_list)
