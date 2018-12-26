# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class FirstNameCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(FirstNameCase, cls).setUpClass()
        cls.lead_model = cls.env["crm.lead"]
        cls.partner_model = cls.env["res.partner"]
        cls.lead = cls.lead_model.create({
            "name": "Léad",
            "partner_name": "Pärtner",
            "contact_name": "Firçt name",
            "contact_lastname": "Laçt name",
        })
        cls.partner = cls.partner_model.create({
            "firstname": "Firçt name",
            "lastname": "Laçt name",
        })

    def test_create_contact(self):
        """Contact correctly created."""
        partner_id = self.lead.handle_partner_assignation()[self.lead.id]
        partner = self.partner_model.browse(partner_id)
        self.assertEqual(self.lead.contact_name, partner.firstname)
        self.assertEqual(self.lead.contact_lastname, partner.lastname)

    def test_create_contact_empty(self):
        """No problems creating a contact without names."""
        self.lead.write({
            "contact_name": False,
            "contact_lastname": False,
        })
        self.lead.handle_partner_assignation()

    def test_onchange_partner(self):
        """When changing partner, fields get correctly updated."""
        with self.env.do_in_onchange():
            self.lead.partner_id = self.partner
            value = self.lead._onchange_partner_id_values(self.partner.id)
            self.assertEqual(
                self.partner.firstname, value["contact_name"])
            self.assertEqual(
                self.partner.lastname, value["contact_lastname"])
