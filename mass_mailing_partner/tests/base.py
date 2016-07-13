# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseCase(TransactionCase):
    def setUp(self):
        super(BaseCase, self).setUp()
        m_partner_category = self.env['res.partner.category']
        m_mailing_list = self.env['mail.mass_mailing.list']
        self.company_id = self.env.ref('base.main_company')
        self.company = self.env['res.company'].browse(self.company_id)
        self.partner = self.create_partner({'name': 'Partner test',
                                            'email': 'partner@test.com'})
        partner_category = m_partner_category.create({'name': 'Category Test'})
        self.mailing_list = m_mailing_list.create({'name': 'List test'})
        self.mailing_list2 = m_mailing_list.create(
            {'name': 'List test 2', 'partner_mandatory': True,
             'partner_category': partner_category.id})

    def create_partner(self, vals):
        m_partner = self.env['res.partner']
        return m_partner.create(vals)

    def create_mailing_contact(self, vals):
        m_mailing_contact = self.env['mail.mass_mailing.contact']
        return m_mailing_contact.create(vals)

    def check_mailing_contact_partner(self, mailing_contact):
        if mailing_contact.partner_id:
            self.assertEqual(mailing_contact.partner_id.email,
                             mailing_contact.email)
            self.assertEqual(mailing_contact.partner_id.name,
                             mailing_contact.name)
