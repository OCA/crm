# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def set_values(self):
        crm_lead = self.env["crm.lead"]
        applied_currency = crm_lead._get_multicompany_reporting_currency_id()
        super().set_values()
        to_apply_currency = self.multicompany_reporting_currency
        if applied_currency.id != to_apply_currency.id:
            crm_lead.with_context(active_test=False).search([]).write(
                {"multicompany_reporting_currency_id": to_apply_currency.id}
            )
        return True
