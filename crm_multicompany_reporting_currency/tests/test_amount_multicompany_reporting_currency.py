# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)


from odoo import fields
from odoo.tests.common import TransactionCase

from odoo.addons.mail.tests.common import mail_new_test_user


class TestAmountMulticompanyReportingCurrency(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.currency_swiss_id = cls.env.ref("base.CHF").id
        cls.currency_euro_id = cls.env.ref("base.EUR").id
        cls.belgium = cls.env.ref("base.be").id
        cls.company = cls.env["res.company"].create({"name": "My company"})
        cls.company.currency_id = cls.currency_euro_id
        cls.user_sales_salesman = mail_new_test_user(
            cls.env,
            login="user_sales_salesman_1",
            name="John Doe",
            email="crm_salesman_1@test.example.com",
            company_id=cls.company.id,
            notification_type="inbox",
            groups="sales_team.group_sale_salesman",
        )
        cls.env["res.currency.rate"].create(
            {
                "name": fields.Date.today(),
                "rate": 1.0038,
                "currency_id": cls.currency_swiss_id,
                "company_id": cls.company.id,
            }
        )
        cls.env["res.currency.rate"].create(
            {
                "name": fields.Date.today(),
                "rate": 1,
                "currency_id": cls.currency_euro_id,
                "company_id": cls.company.id,
            }
        )

    def test_amount_multicompany_reporting_currency(self):
        # Company currency is in EUR, Amount Multicompany Reporting Currency is CHF
        self.env["res.config.settings"].create(
            {"multicompany_reporting_currency": self.currency_swiss_id}
        ).execute()
        self.lead_1 = (
            self.env["crm.lead"]
            .with_company(self.company)
            .create(
                {
                    "name": "Lead 1",
                    "user_id": self.user_sales_salesman.id,
                    "country_id": self.belgium,
                    "expected_revenue": 1000,
                }
            )
        )
        self.assertAlmostEqual(
            self.lead_1.amount_multicompany_reporting_currency, 1003.8
        )
        # Company currency is in EUR, Amount Multicompany Reporting Currency is EUR
        self.env["res.config.settings"].create(
            {"multicompany_reporting_currency": self.currency_euro_id}
        ).execute()
        self.lead_2 = (
            self.env["crm.lead"]
            .with_company(self.company)
            .create(
                {
                    "name": "Lead 2",
                    "user_id": self.user_sales_salesman.id,
                    "country_id": self.belgium,
                    "expected_revenue": 1230,
                }
            )
        )
        self.assertAlmostEqual(self.lead_2.amount_multicompany_reporting_currency, 1230)
        # Company isn't set on the Lead, Amount Multicompany Reporting Currency is EUR
        self.lead_2 = self.env["crm.lead"].create(
            {
                "name": "Lead 2",
                "user_id": self.user_sales_salesman.id,
                "country_id": self.belgium,
                "expected_revenue": 842,
            }
        )
        self.assertAlmostEqual(self.lead_2.amount_multicompany_reporting_currency, 842)
