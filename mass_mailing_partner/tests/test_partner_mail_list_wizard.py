# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import base
from openerp.exceptions import Warning as UserError


class PartnerMailListWizardCase(base.BaseCase):

    def test_add_to_mail_list(self):
        wizard = self.env['partner.mail.list.wizard'].create(
            {'mail_list_id': self.mailing_list.id})
        wizard.partner_ids = [self.partner.id]
        wizard.add_to_mail_list()
        contact = self.env['mail.mass_mailing.contact'].search([
            ('partner_id', '=', self.partner.id),
            ('list_id', '=', self.mailing_list.id)])
        self.check_mailing_contact_partner(contact)
        # This line does not create a new contact
        wizard.add_to_mail_list()
        partner = self.env['res.partner'].create({'name': 'No email partner'})
        wizard.partner_ids = [partner.id]
        with self.assertRaises(UserError):
            wizard.add_to_mail_list()
