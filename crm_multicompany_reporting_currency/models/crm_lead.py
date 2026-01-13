# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "multicompany.reporting.currency.mixin"]

    amount_multicompany_reporting_currency = fields.Monetary(
        currency_field="multicompany_reporting_currency_id",
        compute="_compute_amount_multicompany_reporting_currency",
        store=True,
    )

    @api.depends(
        "create_date",
        "expected_revenue",
        # Dependency on ``crm_lead_company_currency_fix`` grants this field is stored
        "company_currency",
        # Inherited from ``multicompany.reporting.currency.mixin``
        "multicompany_reporting_currency_id",
    )
    def _compute_amount_multicompany_reporting_currency(self):
        for lead in self:
            amount = lead.expected_revenue
            from_curr = lead.company_currency
            to_curr = lead.multicompany_reporting_currency_id
            if from_curr != to_curr:
                amount = from_curr._convert(
                    from_amount=amount,
                    to_currency=to_curr,
                    # Let ``res.currency._convert()`` handle company and date if empty
                    company=lead.company_id or None,
                    date=lead.create_date or None,
                    # Leave roundings to field's ``convert_to_[cache|column_insert]()``
                    round=False,
                )
            lead.amount_multicompany_reporting_currency = amount
