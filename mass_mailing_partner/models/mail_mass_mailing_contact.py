# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields, api, _


class MailMassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner",
                                 domain=[('email', '!=', False)])

    _sql_constraints = [
        ('partner_list_uniq', 'unique(partner_id, list_id)',
         _('Partner already exists in this mailing list.'))
    ]

    @api.one
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.name = self.partner_id.name
            self.email = self.partner_id.email

    @api.model
    @api.returns('self', lambda x: x.id)
    def create(self, vals):
        if not vals.get('partner_id'):
            vals = self._set_partner(vals)
        vals = self._set_name_email(vals)
        return super(MailMassMailingContact, self).create(vals)

    @api.one
    def write(self, vals):
        if vals.get('partner_id', None) is False:
            # If removing partner, search again by email
            vals = self._set_partner(vals)
        vals = self._set_name_email(vals)
        return super(MailMassMailingContact, self).write(vals)

    def _prepare_partner(self, vals, mailing_list):
        vals = {
            'name': vals.get('name') or vals.get('email'),
            'email': vals.get('email', False),
        }
        if mailing_list.partner_category:
            vals['category_id'] = [(4, mailing_list.partner_category.id, 0)]
        return vals

    def _set_partner(self, vals):
        email = vals.get('email', self.email)
        if not email:
            return vals
        m_mailing = self.env['mail.mass_mailing.list']
        m_partner = self.env['res.partner']
        list_id = vals.get('list_id', self.list_id.id)
        mailing_list = m_mailing.browse(list_id)
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

    def _set_name_email(self, vals):
        partner_id = vals.get('partner_id', self.partner_id.id)
        if not partner_id:
            return vals
        partner = self.env['res.partner'].browse(partner_id)
        vals['email'] = partner.email
        vals['name'] = partner.name
        return vals
