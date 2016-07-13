# -*- coding: utf-8 -*-
# © 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import base


class MailMailStatisticsCase(base.BaseCase):

    def test_link_partner(self):
        partner = self.create_partner(
            {'name': 'Test partner'})
        stat = self.env['mail.mail.statistics'].create({
            'model': 'res.partner',
            'res_id': partner.id,
        })
        self.assertEqual(partner.id, stat.partner_id.id)

    def test_link_mail_contact(self):
        partner = self.create_partner(
            {'name': 'Test partner', 'email': 'test@domain.com'})
        contact = self.create_mailing_contact(
            {'partner_id': partner.id, 'list_id': self.mailing_list.id})
        stat = self.env['mail.mail.statistics'].create({
            'model': 'mail.mass_mailing.contact',
            'res_id': contact.id,
        })
        self.assertEqual(partner.id, stat.partner_id.id)
