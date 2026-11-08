# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import users

from .common import Common


class TestCRMLeadCompanyCurrencyFix(Common):
    @users("user_eur")
    def test_00_lead_currency_preserved_after_company_currency_changes(self):
        # Prepare the same values to use for 2 leads, one created before the currency
        # update on the company, one after that
        vals = {"name": "Lead", "company_id": self.company_eur.id}

        # Make sure that if you change the currency on the lead's company after the lead
        # has already been created won't update the currency on the lead itself
        lead_1 = self.env["crm.lead"].create(vals)
        self._test_lead_company_currency(lead_1, self.currency_eur)
        self.company_eur.currency_id = self.currency_chf
        self._test_lead_company_currency(lead_1, self.currency_eur)

        # Check that a newly created lead will use the new currency instead
        lead_2 = self.env["crm.lead"].create(vals)
        self._test_lead_company_currency(lead_2, self.currency_chf)

    def test_01_currency_consistency_for_lead_without_company(self):
        # Let the EUR user create a lead with no company
        lead = (
            self.env["crm.lead"]
            .with_user(self.user_eur)
            .create(
                {
                    "name": "Lead",
                    "company_id": False,
                    # Keep ``user_id`` empty to prevent ``AccessError`` when
                    # trying to read the lead's currency with the CHF user
                    "user_id": False,
                }
            )
        )

        # Check the company is EUR for both EUR user and CHF user
        self._test_lead_company_currency(lead, self.currency_eur, self.user_eur)
        self._test_lead_company_currency(lead, self.currency_eur, self.user_chf)
