# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import base
from openerp.exceptions import ValidationError


class ResPartnerCase(base.BaseCase):

    def test_count_mass_mailing_contacts(self):
        self.create_mailing_contact({'email': 'partner@test.com',
                                     'list_id': self.mailing_list.id})
        self.create_mailing_contact({'email': 'partner@test.com',
                                     'list_id': self.mailing_list2.id})
        self.assertEqual(self.partner.mass_mailing_contacts_count, 2)

    def test_write_res_partner(self):
        contact = self.create_mailing_contact(
            {'email': 'partner@test.com', 'list_id': self.mailing_list.id})
        self.partner.write({'name': 'Changed', 'email': 'partner@changed.com'})
        self.assertEqual(contact.name, self.partner.name)
        self.assertEqual(contact.email, self.partner.email)
        with self.assertRaises(ValidationError):
            self.partner.write({'email': False})
