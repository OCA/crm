# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Antonio Espinosa
# See README.rst file on addon root folder for more details

from openerp import models, fields


class MailMassMailingTest(models.Model):
    _inherit = 'mail.mass_mailing.test'

    mass_mailing_id = fields.Many2one(ondelete='cascade')
