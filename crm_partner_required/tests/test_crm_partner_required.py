# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestCRMPartnerRequired(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

    def test_crm_partner_required(self):
        """Check partner_id required in opportunity"""
        # Check required in opportunity in default form
        opportunity_form = Form(
            self.env["crm.lead"].with_context(default_type="opportunity")
        )
        opportunity_form.name = "Test Opportunity"
        with self.assertRaises(AssertionError):
            opportunity_form.save()
        opportunity_form.partner_id = self.partner
        opportunity_form.save()
        # Check required in opportunity in quick create form
        opportunity_quick_create_form = Form(
            self.env["crm.lead"].with_context(default_type="opportunity"),
            "crm.quick_create_opportunity_form",
        )
        opportunity_quick_create_form.name = "Test Opportunity Quick Create"
        with self.assertRaises(AssertionError):
            opportunity_quick_create_form.save()
        opportunity_quick_create_form.partner_id = self.partner
        opportunity_quick_create_form.save()
        # Check required in lead in default form
        lead_form = Form(self.env["crm.lead"].with_context(default_type="lead"))
        lead_form.name = "Test Lead"
        lead_form.save()
