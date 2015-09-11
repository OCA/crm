# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields


class MailMassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    partner_mandatory = fields.Boolean(string="Mandatory Partner",
                                       default=False)
    partner_category = fields.Many2one(comodel_name='res.partner.category',
                                       string="Partner Tag")
