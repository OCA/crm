# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCrmKlaviyo(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp()
        self.other_company = self.env.user.company_id.create({
            'name': 'Other company',
        })
        self.account_with_company = self.env['klaviyo.account'].create({
            'api_key': 'with_company',
            'company_id': self.other_company.id,
        })
        self.account_without_company = self.env['klaviyo.account'].create({
            'api_key': 'without_company',
        })

    def test_account_selection(self):
        """Test company selection"""
        client = self.env['klaviyo.account'].get_api()
        self.assertEqual(client.api_key, 'without_company')
        client = self.env['klaviyo.account'].get_api(self.other_company)
        self.assertEqual(client.api_key, 'with_company')
