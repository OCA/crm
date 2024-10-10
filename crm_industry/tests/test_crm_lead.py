# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestCrmLead(TransactionCase):
    def test_check_industries(self):
        industry = self.env["res.partner.industry"].create({"name": "Test"})
        with self.assertRaises(UserError):
            self.env["crm.lead"].create(
                {
                    "name": "Test",
                    "industry_id": industry.id,
                    "secondary_industry_ids": [(4, industry.id)],
                }
            )

    def test_lead_create_contact(self):
        industry_pool = self.env["res.partner.industry"]
        industry_1 = industry_pool.create({"name": "Test 01"})
        industry_2 = industry_pool.create(
            {"name": "Test 02", "parent_id": industry_1.id}
        )
        industry_3 = industry_pool.create(
            {"name": "Test 03", "parent_id": industry_1.id}
        )
        lead_vals = {
            "name": "test",
            "partner_name": "test",
            "industry_id": industry_1.id,
            "secondary_industry_ids": [(4, industry_2.id, 0), (4, industry_3.id, 0)],
        }
        lead = self.env["crm.lead"].create(lead_vals)
        partner = self.env["res.partner"].create(
            lead._prepare_customer_values(lead.partner_name, is_company=True)
        )
        self.assertEqual(partner.industry_id, lead.industry_id)
        self.assertEqual(partner.secondary_industry_ids, lead.secondary_industry_ids)

    def test_propagate_industries_from_contact(self):
        res_partner_industry = self.env["res.partner.industry"]
        industry_1 = res_partner_industry.create({"name": "IT/Communications"})
        industry_2 = res_partner_industry.create(
            {"name": "AI/Machine Learning", "parent_id": industry_1.id}
        )
        industry_3 = res_partner_industry.create(
            {"name": "ERP Systems", "parent_id": industry_1.id}
        )
        customer = self.env["res.partner"].create(
            {
                "name": "Test Customer",
                "industry_id": industry_1.id,
                "secondary_industry_ids": [
                    (4, industry_2.id, 0),
                    (4, industry_3.id, 0),
                ],
            }
        )
        lead_form = Form(self.env["crm.lead"])
        lead_form.name = "Test Lead"
        lead_form.partner_id = customer
        lead = lead_form.save()
        self.assertEqual(lead.industry_id, customer.industry_id)
        self.assertEqual(lead.secondary_industry_ids, customer.secondary_industry_ids)
