# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    mass_mailing_contacts = fields.One2many(
        comodel_name='mail.mass_mailing.contact', inverse_name='partner_id')

    mass_mailing_contacts_count = fields.Integer(
        string='Mailing list number', compute='_count_mass_mailing_contacts',
        store=True)

    @api.one
    @api.constrains('email')
    def _check_email_mass_mailing_contacts(self):
        if self.mass_mailing_contacts and not self.email:
            raise ValidationError(
                _("This partner '%s' is subscribed to one or more "
                  "mailing lists. Email must be assigned." % self.name))

    @api.one
    @api.depends('mass_mailing_contacts')
    def _count_mass_mailing_contacts(self):
        self.mass_mailing_contacts_count = len(self.mass_mailing_contacts)

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if vals.get('name') or vals.get('email'):
            mm_vals = {}
            if vals.get('name'):
                mm_vals['name'] = vals['name']
            if vals.get('email'):
                mm_vals['name'] = vals['email']
            self.mapped('mass_mailing_contacts').write(mm_vals)
        return res
