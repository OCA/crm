# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests.common import TransactionCase


class CRMLead(TransactionCase):
    def test_crm_lead_date_partner_assign(self):
        """Test that `date_partner_assign` is set when assigning a partner."""
        lead = self.env["crm.lead"].create(
            {
                "name": "Lead 1",
                "partner_contact_assigned_id": self.env["res.partner"]
                .create(
                    {
                        "name": "Partner 1",
                    }
                )
                .id,
            }
        )
        self.assertTrue(lead.date_partner_assign)
