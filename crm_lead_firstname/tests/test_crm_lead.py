# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import Form, SavepointCase


class FirstNameCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(FirstNameCase, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.lead_model = cls.env["crm.lead"]
        cls.partner_model = cls.env["res.partner"]
        cls.lead = cls.lead_model.create(
            {
                "name": "Léad",
                "partner_name": "Pärtner",
                "contact_name": "Firçt name",
                "contact_lastname": "Laçt name",
            }
        )
        cls.partner = cls.partner_model.create(
            {"firstname": "Firçt name", "lastname": "Laçt name"}
        )

    def test_create_contact(self):
        """Contact correctly created."""
        partner_id = self.lead.handle_partner_assignation()[self.lead.id]
        partner = self.partner_model.browse(partner_id)
        self.assertEqual(self.lead.contact_name, partner.firstname)
        self.assertEqual(self.lead.contact_lastname, partner.lastname)

    def test_create_contact_empty(self):
        """No problems creating a contact without names."""
        self.lead.write({"contact_name": False, "contact_lastname": False})
        self.lead.handle_partner_assignation()

    def test_onchange_partner(self):
        """When changing partner, fields get correctly updated."""
        with Form(self.env["crm.lead"], view="crm.crm_lead_view_form") as lead_form:
            lead_form.partner_id = self.partner
            lead_form.name = self.partner.name
            lead_form.save()
            self.assertEqual(self.partner.firstname, lead_form.contact_name)
            self.assertEqual(self.partner.lastname, lead_form.contact_lastname)
