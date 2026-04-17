# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestCRMDateDeadlineRequired(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_crm_date_deadline_required_opportunity(self):
        """Check date_deadline is required in opportunity default form."""
        opportunity_form = Form(
            self.env["crm.lead"].with_context(default_type="opportunity")
        )
        opportunity_form.name = "Test Opportunity"
        # The Form object raises AssertionError for XML required fields
        # before the server-side ValidationError can be triggered.
        with self.assertRaises(AssertionError):
            opportunity_form.save()
        opportunity_form.date_deadline = "2025-01-01"
        opportunity_form.save()

    def test_crm_date_deadline_required_opportunity_quick_create(self):
        """Check date_deadline is required via server validation for quick create."""
        # We test the server constraint directly because the field
        # was removed from the quick create view to fix the OWL UI bug.
        with self.assertRaises(ValidationError):
            self.env["crm.lead"].with_context(default_type="opportunity").create(
                {
                    "name": "Test Opportunity Quick Create",
                    "type": "opportunity",
                    # We omit date_deadline to trigger the Python ValidationError
                }
            )

    def test_crm_date_deadline_required_lead(self):
        """Check date_deadline is not required for lead types."""
        lead_form = Form(self.env["crm.lead"].with_context(default_type="lead"))
        lead_form.name = "Test Lead"
        # Should save without errors as it's not an opportunity
        lead_form.save()
