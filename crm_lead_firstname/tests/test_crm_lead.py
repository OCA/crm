# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class FirstnameCase(TransactionCase):
    def setUp(self):
        super(FirstnameCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": u"Léad",
            "partner_name": u"Pärtner",
            "contact_name": u"Firçt name",
            "contact_lastname": u"Laçt name",
        })
        self.partner = self.env["res.partner"].create({
            "firstname": u"Firçt name",
            "lastname": u"Laçt name",
        })

    def test_create_contact(self):
        """Contact correctly created."""
        partner_id = self.lead.handle_partner_assignation()[self.lead.id]
        partner = self.env["res.partner"].browse(partner_id)
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
            value = self.lead.on_change_partner_id(self.partner.id)["value"]
            self.assertEqual(
                self.partner.firstname, value["contact_name"])
            self.assertEqual(
                self.partner.lastname, value["contact_lastname"])
