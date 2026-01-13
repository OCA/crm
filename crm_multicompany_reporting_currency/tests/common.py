# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.addons.base_multicompany_reporting_currency.tests.common import (
    Common as BaseMulticompanyReportingCurrencyCommon,
)
from odoo.addons.crm_lead_company_currency_fix.tests.common import (
    Common as CrmLeadCompanyCurrencyFixCommon,
)


class Common(BaseMulticompanyReportingCurrencyCommon, CrmLeadCompanyCurrencyFixCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup currencies rates
        yesterday = date.today() - relativedelta(days=1)
        cls.env["res.currency.rate"].create(
            [
                {
                    "name": yesterday,
                    "rate": 0.80,  # 1.00 EUR = 0.80 CHF
                    "currency_id": cls.currency_chf.id,
                    "company_id": cls.company_eur.id,
                },
                {
                    "name": yesterday,
                    "rate": 1.25,  # 1.00 CHF = 1.25 EUR
                    "currency_id": cls.currency_eur.id,
                    "company_id": cls.company_chf.id,
                },
            ]
        )
