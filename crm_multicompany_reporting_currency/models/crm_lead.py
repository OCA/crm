# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.fields import Date


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _get_multicompany_reporting_currency_id(self):
        multicompany_reporting_currency_parameter = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "base_multicompany_reporting_currency.multicompany_reporting_currency"
            )
        )
        return self.env["res.currency"].browse(
            int(multicompany_reporting_currency_parameter)
        )

    multicompany_reporting_currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_multicompany_reporting_currency_id",
        readonly=True,
        store=True,
        default=_get_multicompany_reporting_currency_id,
    )
    currency_rate = fields.Float(
        compute="_compute_currency_rate", store=True, digits=(12, 6)
    )
    amount_multicompany_reporting_currency = fields.Monetary(
        currency_field="multicompany_reporting_currency_id",
        compute="_compute_amount_multicompany_reporting_currency",
        store=True,
        index=True,
        readonly=True,
    )

    # technical field to be used in sum_field options on kanban
    current_company_currency = fields.Many2one(
        "res.currency", compute="_compute_current_company_currency", readonly=True
    )

    def _compute_current_company_currency(self):
        for lead in self:
            lead.current_company_currency = self.env.company.currency_id

    @api.depends("company_currency")
    def _compute_multicompany_reporting_currency_id(self):
        multicompany_reporting_currency_id = (
            self._get_multicompany_reporting_currency_id()
        )
        for record in self:
            record.multicompany_reporting_currency_id = (
                multicompany_reporting_currency_id
            )

    @api.depends("create_date", "company_id", "multicompany_reporting_currency_id")
    def _compute_currency_rate(self):
        # similar to currency_rate on sale.order
        for record in self:
            date = record.create_date or fields.Date.today()
            if not record.company_id:
                record.currency_rate = (
                    record.multicompany_reporting_currency_id.with_context(
                        date=date
                    ).rate
                    or 1.0
                )
            elif (
                record.company_currency and record.multicompany_reporting_currency_id
            ):  # the following crashes if any one is undefined
                record.currency_rate = self.env["res.currency"]._get_conversion_rate(
                    record.company_currency,
                    record.multicompany_reporting_currency_id,
                    record.company_id,
                    date,
                )
            else:
                record.currency_rate = 1.0

    @api.depends(
        "expected_revenue", "currency_rate", "multicompany_reporting_currency_id"
    )
    def _compute_amount_multicompany_reporting_currency(self):
        for record in self:
            if record.company_currency == record.multicompany_reporting_currency_id:
                to_amount = record.expected_revenue
            else:
                to_amount = record.expected_revenue * record.currency_rate
            record.amount_multicompany_reporting_currency = to_amount

    @api.model
    def read_group(self, domain, fields, groupby, **kwargs):
        # Override read_group to calculate the sum of the
        # expected revenue in current company currency
        current_company = self.env.company
        result = super().read_group(
            domain,
            fields,
            groupby,
            **kwargs,
        )
        opportunities = self.env["crm.lead"]
        for line in result:
            if "__domain" in line:
                opportunities = self.search(line["__domain"])

            if "expected_revenue" in fields:
                global_revenue = sum(
                    opportunities.mapped(
                        lambda opp: opp.company_currency._convert(
                            opp.expected_revenue,
                            current_company.currency_id,
                            current_company,
                            Date.today(),
                        )
                    )
                )
                line["expected_revenue"] = global_revenue
        return result
