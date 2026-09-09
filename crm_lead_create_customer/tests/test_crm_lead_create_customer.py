# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase


class TestCrmLeadCreateCustomer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def _new_opportunity(self, **values):
        opportunity_form = Form(
            self.env["crm.lead"].with_context(default_type="opportunity")
        )
        opportunity_form.name = values.pop("name", "Website enquiry")
        for field_name, value in values.items():
            setattr(opportunity_form, field_name, value)
        return opportunity_form.save()

    def _open_wizard(self, opportunity):
        """Open the wizard the way the Create Customer button does."""
        action = opportunity.action_create_customer()
        self.assertEqual(action["res_model"], "crm.lead2opportunity.partner")
        return Form(
            self.env[action["res_model"]].with_context(**action["context"]),
            view=action["views"][0][0],
        )

    def test_create_customer_from_opportunity(self):
        """An opportunity that never was a lead builds its own customer."""
        opportunity = self._new_opportunity(
            contact_name="John Smith",
            partner_name="Odoo S.A.",
            email_from="john@smith.example.com",
            phone="+32 494 12 34 56",
            city="Grand-Rosiere",
        )
        self.assertEqual(opportunity.type, "opportunity")
        self.assertFalse(opportunity.partner_id)

        wizard_form = self._open_wizard(opportunity)
        self.assertEqual(wizard_form.action, "create")
        wizard_form.save().action_apply()

        customer = opportunity.partner_id
        self.assertEqual(customer.name, "John Smith")
        self.assertEqual(customer.email, "john@smith.example.com")
        self.assertEqual(customer.city, "Grand-Rosiere")
        self.assertTrue(customer.parent_id.is_company)
        self.assertEqual(customer.parent_id.name, "Odoo S.A.")
        self.assertEqual(opportunity.type, "opportunity")

    def test_wizard_defaults_to_linking_the_matching_customer(self):
        """A partner matching the email is offered instead of a new one."""
        existing = self.partner_model.create(
            {"name": "Existing Customer", "email": "john@smith.example.com"}
        )
        opportunity = self._new_opportunity(
            contact_name="John Smith", email_from="john@smith.example.com"
        )

        wizard_form = self._open_wizard(opportunity)
        self.assertEqual(wizard_form.action, "exist")
        self.assertEqual(wizard_form.partner_id, existing)
        wizard_form.save().action_apply()

        self.assertEqual(opportunity.partner_id, existing)

    def test_wizard_can_create_instead_of_linking(self):
        """The user can refuse the match and create a new customer."""
        self.partner_model.create(
            {"name": "Existing Customer", "email": "john@smith.example.com"}
        )
        opportunity = self._new_opportunity(
            contact_name="John Smith", email_from="john@smith.example.com"
        )

        wizard_form = self._open_wizard(opportunity)
        wizard_form.action = "create"
        wizard_form.save().action_apply()

        self.assertEqual(opportunity.partner_id.name, "John Smith")
        self.assertNotEqual(opportunity.partner_id.name, "Existing Customer")

    def test_merge_also_creates_the_customer(self):
        """Merging duplicates still has to produce the customer."""
        opportunity = self._new_opportunity(
            contact_name="John Smith",
            partner_name="Odoo S.A.",
            email_from="john@smith.example.com",
        )
        duplicate = self._new_opportunity(
            name="Second enquiry",
            contact_name="John Smith",
            email_from="john@smith.example.com",
        )

        wizard_form = self._open_wizard(opportunity)
        self.assertEqual(wizard_form.name, "merge", "the duplicate should be detected")
        wizard = wizard_form.save()
        self.assertIn(duplicate, wizard.duplicated_lead_ids)
        wizard.action_apply()

        merged = wizard.lead_id
        self.assertEqual(merged.type, "opportunity")
        self.assertTrue(
            merged.partner_id, "merging must not skip the customer creation"
        )
        self.assertEqual(merged.partner_id.name, "John Smith")

    def test_merge_can_be_declined(self):
        """Unticking the box must keep the duplicate as a separate record."""
        opportunity = self._new_opportunity(
            contact_name="John Smith", email_from="john@smith.example.com"
        )
        duplicate = self._new_opportunity(
            name="Second enquiry",
            contact_name="John Smith",
            email_from="john@smith.example.com",
        )

        wizard_form = self._open_wizard(opportunity)
        self.assertTrue(wizard_form.merge_duplicates)
        wizard_form.merge_duplicates = False
        wizard_form.save().action_apply()

        self.assertTrue(duplicate.exists(), "the duplicate must not be merged")
        self.assertTrue(opportunity.partner_id)

    def test_wizard_arch_hides_the_conversion_choice(self):
        """Nothing is converted here, so the convert/merge radio is gone.

        The label cannot come from the field metadata: the web client strips
        the context before loading the views, so it has to be in the arch.
        """
        opportunity = self._new_opportunity(contact_name="John Smith")
        action = opportunity.action_create_customer()
        arch = (
            self.env["crm.lead2opportunity.partner"]
            .get_view(action["views"][0][0], "form")["arch"]
            .encode()
        )
        form = etree.fromstring(arch)
        radio = form.xpath("//group[@name='name']")[0]
        self.assertEqual(radio.get("invisible"), "1")
        checkbox = form.xpath("//field[@name='merge_duplicates']")[0]
        self.assertEqual(
            checkbox.get("string"), "Merge with the duplicate opportunities found"
        )
        # The customer choice must stay reachable while merging.
        self.assertEqual(form.xpath("//div[@name='action']")[0].get("invisible"), "0")
        self.assertNotIn(b"Convert to opportunity", arch)

    def test_create_customer_without_contact_data(self):
        """Refuse to name the customer after the opportunity subject."""
        opportunity = self._new_opportunity()

        with self.assertRaises(UserError):
            opportunity.action_create_customer()
        self.assertFalse(opportunity.partner_id)

    def test_create_customer_already_assigned(self):
        """Refuse to overwrite an already assigned customer."""
        existing = self.partner_model.create({"name": "Existing Customer"})
        opportunity = self._new_opportunity(partner_id=existing)

        with self.assertRaises(UserError):
            opportunity.action_create_customer()
        self.assertEqual(opportunity.partner_id, existing)

    def _lead_form_arch(self):
        arch = self.env["crm.lead"].get_view(
            self.env.ref("crm.crm_lead_view_form").id, "form"
        )["arch"]
        return etree.fromstring(arch.encode())

    def test_opportunity_form_exposes_contact_fields(self):
        """The customer source fields are reachable on the opportunity form."""
        group = self._lead_form_arch().xpath("//group[@name='opportunity_partner']")[0]
        exposed = {
            field.get("name"): field.get("invisible")
            for field in group.xpath(".//field")
        }
        for name in ("contact_name", "partner_name", "function", "website"):
            self.assertEqual(
                exposed.get(name),
                "partner_id",
                f"{name} should be shown on opportunities without a customer",
            )

    def test_create_customer_button_is_in_the_header(self):
        """The button sits in the status bar, next to Won and Lost."""
        header = self._lead_form_arch().xpath("//header")[0]
        buttons = header.xpath("./button")
        names = [button.get("name") for button in buttons]
        self.assertIn("action_create_customer", names)
        button = buttons[names.index("action_create_customer")]
        self.assertEqual(
            button.get("invisible"), "partner_id or type == 'lead' or not active"
        )
        self.assertIn("oe_highlight", button.get("class") or "")
        # Placed among the action buttons, before the stage status bar.
        self.assertLess(
            names.index("action_create_customer"),
            names.index("action_restore"),
        )
