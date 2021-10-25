# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    fax = fields.Char("Fax")

    @api.onchange("fax", "country_id", "company_id")
    def _onchange_phone2_validation(self):
        # Compatibility with phone_validation
        if hasattr(self, "phone_format") and self.fax:
            self.fax = self.phone_format(self.fax)
