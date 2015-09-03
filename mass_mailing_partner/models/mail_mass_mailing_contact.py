# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class MailMassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner",
                                 domain=[('email', '!=', False)])

    @api.one
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.name = self.partner_id.name
            self.email = self.partner_id.email

    @api.one
    @api.constrains('partner_id')
    def _check_partner_id(self):
        """Ensure at least one name is set."""
        if self.partner_id:
            already = self.search([
                ('id', '!=', self.id),
                ('partner_id', '=', self.partner_id.id),
                ('list_id', '=', self.list_id.id),
            ])
            if already:
                raise ValidationError(
                    _('Partner already exists in this mailing list.'))

    @api.model
    def create(self, vals):
        if not vals.get('partner_id'):
            vals = self._check_partner(vals)
        vals = self._check_name_email(vals)
        return super(MailMassMailingContact, self).create(vals)

    @api.one
    def write(self, vals):
        if vals.get('partner_id', None) is False:
            # If removing partner, search again by email
            vals = self._check_partner(vals)
        vals = self._check_name_email(vals)
        return super(MailMassMailingContact, self).write(vals)

    def _prepare_partner(self, vals, mailing_list):
        vals = {
            'name': vals.get('name') or vals.get('email'),
            'email': vals.get('email', False),
        }
        if mailing_list.partner_category:
            vals['category_id'] = [(4, mailing_list.partner_category.id, 0)]
        return vals

    def _check_partner(self, vals):
        m_mailing = self.env['mail.mass_mailing.list']
        m_partner = self.env['res.partner']
        list_id = vals.get('list_id') or self.list_id.id
        email = vals.get('email') or self.email
        mailing_list = m_mailing.browse(list_id)
        if not email:
            return vals
        # Look for a partner with that email
        email = email.strip()
        partners = m_partner.search([('email', '=ilike', email)], limit=1)
        if partners:
            # Partner found
            vals['partner_id'] = partners[0].id
        elif mailing_list.partner_mandatory:
            # Create partner
            partner = m_partner.sudo().create(
                self._prepare_partner(vals, mailing_list))
            vals['partner_id'] = partner.id
        return vals

    def _check_name_email(self, vals):
        partner_id = vals.get('partner_id', None)
        if partner_id is None:
            partner_id = self.partner_id.id
        if not partner_id:
            return vals
        partner = self.env['res.partner'].browse(partner_id)
        vals['email'] = partner.email
        vals['name'] = partner.name
        return vals
