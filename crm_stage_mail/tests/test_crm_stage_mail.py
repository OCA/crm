# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase

from odoo.addons.mail.tests.common import MailCase


class TestCrmStageMail(TransactionCase, MailCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner",
                "email": "test@test.com",
            }
        )
        cls.stage_new = cls.env["crm.stage"].create(
            {
                "name": "New",
                "sequence": 10,
            }
        )
        template = cls.env.ref("crm.mail_template_demo_crm_lead")
        template.subject = "Welcome"
        cls.stage_qualified = cls.env["crm.stage"].create(
            {
                "name": "Qualified",
                "sequence": 20,
                "mail_template_id": template.id,
            }
        )

    def test_crm_lead_new(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": self.partner.id,
                "stage_id": self.stage_new.id,
            }
        )
        self.flush_tracking()
        self.assertNotIn("auto_comment", lead.message_ids.mapped("message_type"))

    def test_crm_lead_qualified(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Test lead",
                "partner_id": self.partner.id,
                "stage_id": self.stage_qualified.id,
            }
        )
        self.flush_tracking()
        lead_message = lead.message_ids.filtered(
            lambda m: m.message_type == "auto_comment"
        )
        self.assertIn("Welcome", lead_message.subject)
