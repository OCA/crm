# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


class CrmLead(models.Model):
    _inherit = ["crm.lead", "base.exception"]
    _name = "crm.lead"
    _order = "main_exception_id asc, name desc"

    def write(self, vals):
        result = super().write(vals)
        # To avoid a recursive call, write()
        if "exception_ids" in vals:
            return result
        self._check_exception()
        return result

    @api.model
    def _reverse_field(self):
        return "crm_lead_ids"

    def _rule_domain(self):
        rule_domain = super()._rule_domain()
        if self.stage_id:
            rule_domain = expression.AND(
                [
                    rule_domain,
                    [
                        "|",
                        ("stage_ids", "in", tuple(self.stage_id.ids)),
                        ("stage_ids", "=", False),
                    ],
                ]
            )
        return rule_domain
