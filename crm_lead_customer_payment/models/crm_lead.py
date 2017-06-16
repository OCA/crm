# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    property_payment_term = fields.Many2one(
        comodel_name='account.payment.term', string='Customer Payment Term',
        help="This payment term will be used instead of the default one for"
             " sale orders and customer invoices",
        company_dependent=True)
    customer_payment_mode = fields.Many2one(
        comodel_name='payment.mode', string='Customer Payment Mode',
        company_dependent=True, domain="[('sale_ok', '=', True)]",
        help="Select the default payment mode for this customer.")

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        return super(CrmLead, self.with_context(
            default_property_payment_term=lead.property_payment_term,
            default_customer_payment_mode=lead.customer_payment_mode)
            )._lead_create_contact(lead, name, is_company, parent_id)

    @api.multi
    def on_change_partner_id(self, partner_id):
        result = super(CrmLead, self).on_change_partner_id(partner_id)
        if not partner_id:
            return result
        partner = self.env['res.partner'].browse(partner_id)
        value = result.setdefault('value', {})
        value.update({
            'property_payment_term':
                partner.property_payment_term.id,
            'customer_payment_mode':
                partner.customer_payment_mode.id,
        })
        return result