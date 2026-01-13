# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import users

from .common import Common


class TestAmountMulticompanyReportingCurrency(Common):
    def test_00_crm_lead_detected_by_multicompany_reporting_currency_mixin(self):
        mcrc_mixin = self.env["multicompany.reporting.currency.mixin"]
        crm_lead = self.env["crm.lead"]
        self.assertIn(
            crm_lead,
            mcrc_mixin._get_multicompany_reporting_currency_inheriting_models(),
        )

    @users("user_eur")
    def test_01_leads_with_same_currencies(self):
        # Set EUR as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(self.currency_eur.id)

        lead_vals = {"name": "Lead", "expected_revenue": 1000}
        exp_vals = {
            "company_id": self.company_eur.id,
            "company_currency": self.currency_eur.id,
            "expected_revenue": 1000.00,
            "multicompany_reporting_currency_id": self.currency_eur.id,
            "amount_multicompany_reporting_currency": 1000.00,
        }

        # Test 3 leads:
        # 1) lead created without ``company_id``:
        #   - user's company is assigned to the lead by default (see method
        #   ``crm.lead._compute_company_id()``)
        #   - ``company_currency`` will be computed as the company currency => EUR
        #   - multicompany reporting currency is EUR
        # 2) lead created with ``company_id = False``:
        #   - no company is set, and it's not recomputed (because an explicit value has
        #   been used at creation)
        #   - ``company_currency`` will be computed as the user company currency => EUR
        #   - multicompany reporting currency is EUR
        # 2) lead created with ``company_id = <EUR company>``:
        #   - company is set
        #   - ``company_currency`` will be computed as the company currency => EUR
        #   - multicompany reporting currency is EUR
        self.assertRecordValues(
            records=self.env["crm.lead"].create(
                [
                    lead_vals,
                    dict(lead_vals, company_id=False),
                    dict(lead_vals, company_id=self.company_eur.id),
                ]
            ),
            expected_values=[
                exp_vals,
                dict(exp_vals, company_id=False),
                exp_vals,
            ],
        )

    @users("user_eur")
    def test_02_leads_with_different_currencies(self):
        # Set CHF as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(self.currency_chf.id)

        lead_vals = {"name": "Lead", "expected_revenue": 1000}
        exp_vals = {
            "company_id": self.company_eur.id,
            "company_currency": self.currency_eur.id,
            "expected_revenue": 1000.00,
            "multicompany_reporting_currency_id": self.currency_chf.id,
            "amount_multicompany_reporting_currency": 800.00,
        }

        # Test 3 leads:
        # 1) lead created without ``company_id``:
        #   - user's company is assigned to the lead by default (see method
        #   ``crm.lead._compute_company_id()``)
        #   - ``company_currency`` will be computed as the company currency => EUR
        #   - multicompany reporting currency is CHF
        # 2) lead created with ``company_id = False``:
        #   - no company is set, and it's not recomputed (because an explicit value has
        #   been used at creation)
        #   - ``company_currency`` will be computed as the user company currency => EUR
        #   - multicompany reporting currency is CHF
        # 2) lead created with ``company_id = <EUR company>``:
        #   - company is set
        #   - ``company_currency`` will be computed as the company currency => EUR
        #   - multicompany reporting currency is CHF
        self.assertRecordValues(
            records=self.env["crm.lead"].create(
                [
                    lead_vals,
                    dict(lead_vals, company_id=False),
                    dict(lead_vals, company_id=self.company_eur.id),
                ]
            ),
            expected_values=[
                exp_vals,
                dict(exp_vals, company_id=False),
                exp_vals,
            ],
        )

    @users("user_eur")
    def test_03_check_amount_when_lead_company_currency_changes(self):
        # Set EUR as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(self.currency_eur.id)

        # Create a lead with the EUR company (inherited from the user)
        lead = self.env["crm.lead"].create({"name": "Lead", "expected_revenue": 1000})
        self.assertRecordValues(
            lead,
            [
                {
                    "company_id": self.company_eur.id,
                    "company_currency": self.currency_eur.id,
                    "expected_revenue": 1000.00,
                    "multicompany_reporting_currency_id": self.currency_eur.id,
                    "amount_multicompany_reporting_currency": 1000.00,
                },
            ],
        )

        # Change the lead to the CHF company
        lead.company_id = self.company_chf
        self.assertRecordValues(
            lead,
            [
                {
                    "company_id": self.company_chf.id,
                    "company_currency": self.currency_chf.id,
                    "expected_revenue": 1000.00,
                    "multicompany_reporting_currency_id": self.currency_eur.id,
                    "amount_multicompany_reporting_currency": 1250.00,
                },
            ],
        )

    @users("user_chf")
    def test_04_check_amount_when_multicompany_reporting_currency_changes(self):
        # Set EUR as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(self.currency_eur.id)

        # Create a lead with the CHF company (inherited from the user)
        lead = self.env["crm.lead"].create({"name": "Lead", "expected_revenue": 1000})
        self.assertRecordValues(
            lead,
            [
                {
                    "company_id": self.company_chf.id,
                    "company_currency": self.currency_chf.id,
                    "expected_revenue": 1000.00,
                    "multicompany_reporting_currency_id": self.currency_eur.id,
                    "amount_multicompany_reporting_currency": 1250.00,
                },
            ],
        )

        # Set CHF as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(self.currency_chf.id)
        self.assertRecordValues(
            lead,
            [
                {
                    "company_id": self.company_chf.id,
                    "company_currency": self.currency_chf.id,
                    "expected_revenue": 1000.00,
                    "multicompany_reporting_currency_id": self.currency_chf.id,
                    "amount_multicompany_reporting_currency": 1000.00,
                },
            ],
        )
