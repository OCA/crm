# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestCrmLeadMobile(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner", "mobile": "+55 11 99999-0001"}
        )

    def _test_form(self, view):
        form = Form(
            self.env["crm.lead"].with_context(default_type="opportunity"),
            view=view,
        )
        form.name = "Test Opportunity"
        form.partner_id = self.partner
        self.assertEqual(form.mobile, "+55 11 99999-0001")
        form.mobile = "+55 21 98888-7777"
        lead = form.save()
        self.assertEqual(lead.mobile, "+55 21 98888-7777")
        self.assertEqual(self.partner.mobile, "+55 11 99999-0001")

    def test_opportunity_form(self):
        self._test_form("crm.crm_lead_view_form")

    def test_quick_create_form(self):
        self._test_form("crm.quick_create_opportunity_form")
