# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import base
from ..hooks import post_init_hook
from psycopg2 import IntegrityError


class MailMassMailingContactCase(base.BaseCase):

    def test_match_existing_contacts(self):
        contact = self.create_mailing_contact(
            {'email': 'partner@test.com', 'list_id': self.mailing_list.id})
        post_init_hook(self.cr, self.registry)
        self.assertEqual(contact.partner_id.id, self.partner.id)

    def test_create_mass_mailing_contact(self):
        contact = self.create_mailing_contact(
            {'email': 'partner2@test.com', 'name': 'Partner test 2',
             'list_id': self.mailing_list2.id})
        self.check_mailing_contact_partner(contact)
        with self.assertRaises(IntegrityError):
            self.create_mailing_contact({'email': 'partner2@test.com',
                                         'list_id': self.mailing_list2.id})

    def test_write_mass_mailing_contact(self):
        contact = self.create_mailing_contact(
            {'email': 'partner@test.com', 'list_id': self.mailing_list.id})
        contact.write({'partner_id': False})
        self.check_mailing_contact_partner(contact)
        contact2 = self.create_mailing_contact(
            {'email': 'partner2@test.com', 'name': 'Partner test 2',
             'list_id': self.mailing_list.id})
        contact.write({'partner_id': False})
        self.assertFalse(contact2.partner_id)

    def test_onchange_partner(self):
        contact = self.create_mailing_contact(
            {'email': 'partner@test.com', 'list_id': self.mailing_list.id})
        partner = self.create_partner(
            {'name': 'Test partner', 'email': 'sample@test.com'})
        with self.env.do_in_onchange():
            contact.partner_id = partner
            contact._onchange_partner()
            self.assertEqual(contact.name, partner.name)
            self.assertEqual(contact.email, partner.email)
