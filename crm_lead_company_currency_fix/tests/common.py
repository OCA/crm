# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.orm.commands import Command
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class Common(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup EUR currency and company
        cls.currency_eur = cls.env.ref("base.EUR")
        cls.company_eur = cls.env["res.company"].create({"name": "Company EUR"})
        cls.company_eur.currency_id = cls.currency_eur
        # Setup CHF currency and company
        cls.currency_chf = cls.env.ref("base.CHF")
        cls.company_chf = cls.env["res.company"].create({"name": "Company CHF"})
        cls.company_chf.currency_id = cls.currency_chf
        # Setup test users, making sure they have access to both companies but are
        # logged in to different companies by default
        cls.user_eur = new_test_user(
            cls.env,
            login="user_eur",
            groups="sales_team.group_sale_salesman",
            **dict(
                name="User EUR",
                email="user-eur@test.com",
                company_id=cls.company_eur.id,
                company_ids=[Command.set((cls.company_eur + cls.company_chf).ids)],
            ),
        )
        cls.user_chf = new_test_user(
            cls.env,
            login="user_chf",
            groups="sales_team.group_sale_salesman",
            **dict(
                name="User chf",
                email="user-chf@test.com",
                company_id=cls.company_chf.id,
                company_ids=[Command.set((cls.company_eur + cls.company_chf).ids)],
            ),
        )

    def _test_lead_company_currency(self, lead, expected_currency, user=None):
        lead = lead.with_user(user or self.env.user)
        self.assertEqual(lead.company_currency, expected_currency)
