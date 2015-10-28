# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from . import base
from .. import _match_existing_contacts
from psycopg2 import IntegrityError


class MailMassMailingContactCase(base.BaseCase):

    def test_match_existing_contacts(self):
        contact = self.create_mailing_contact(
            {'email': 'partner@test.com', 'list_id': self.mailing_list.id})
        _match_existing_contacts(self.cr, self.registry)
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
