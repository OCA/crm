# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestCrmLead(BaseCommon):
    _test_user_groups = ("sales_team.group_sale_salesman",)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Salesmen can only read industries, so create them as admin
        industry_model = cls.env["res.partner.industry"]
        cls.industry_main = industry_model.create({"name": "IT/Communications"})
        cls.industry_1 = industry_model.create(
            {"name": "AI/Machine Learning", "parent_id": cls.industry_main.id}
        )
        cls.industry_2 = industry_model.create(
            {"name": "ERP Systems", "parent_id": cls.industry_main.id}
        )
        cls.industry_3 = industry_model.create(
            {"name": "Cloud Services", "parent_id": cls.industry_main.id}
        )
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
                "industry_id": cls.industry_main.id,
                "secondary_industry_ids": [
                    Command.set([cls.industry_1.id, cls.industry_2.id])
                ],
            }
        )

    def test_check_industries(self):
        with self.assertRaises(UserError):
            self.env["crm.lead"].create(
                {
                    "name": "Test",
                    "industry_id": self.industry_main.id,
                    "secondary_industry_ids": [Command.link(self.industry_main.id)],
                }
            )

    def test_lead_create_contact(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "test",
                "partner_name": "test",
                "industry_id": self.industry_main.id,
                "secondary_industry_ids": [
                    Command.set([self.industry_1.id, self.industry_2.id])
                ],
            }
        )
        partner = lead._create_customer()
        self.assertEqual(partner.industry_id, lead.industry_id)
        self.assertEqual(partner.secondary_industry_ids, lead.secondary_industry_ids)

    def test_propagate_industries_from_contact(self):
        lead_form = Form(self.env["crm.lead"])
        lead_form.name = "Test Lead"
        lead_form.partner_id = self.customer
        lead = lead_form.save()
        self.assertEqual(lead.industry_id, self.customer.industry_id)
        self.assertEqual(
            lead.secondary_industry_ids, self.customer.secondary_industry_ids
        )

    def test_create_with_partner_does_not_override_explicit_vals(self):
        lead_form = Form(self.env["crm.lead"])
        lead_form.name = "Test lead"
        lead_form.partner_id = self.customer
        lead_form.industry_id = self.industry_2
        lead_form.secondary_industry_ids.clear()
        lead_form.secondary_industry_ids.add(self.industry_3)
        lead = lead_form.save()
        self.assertEqual(lead.industry_id, self.industry_2)
        self.assertEqual(lead.secondary_industry_ids, self.industry_3)
