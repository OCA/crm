# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


SQL_CONTRACT_COUNT = """
SELECT COALESCE(SUM(ROUND(l.quantity)::integer), 0) as quantity
 FROM account_analytic_invoice_line l
 JOIN account_analytic_account c
 ON l.analytic_account_id = c.id
 WHERE l.product_id = %s
 AND c.partner_id = %s"""

SQL_ASSIGNED_COUNT = """
SELECT COALESCE(SUM(copies), 0) as copies
 FROM distribution_list
 WHERE product_id = %s
 AND contract_partner_id = %s"""


class DistributionList(models.Model):
    _name = 'distribution.list'
    _order = 'name'

    @api.model
    def get_product_contract_count(self, product_id, contract_partner_id):
        self.env.cr.execute(
            SQL_CONTRACT_COUNT,
            (product_id, contract_partner_id))
        return self.env.cr.fetchone()[0]

    @api.model
    def get_product_contract_assigned_count(
            self, product_id, contract_partner_id):
        self.env.cr.execute(
            SQL_ASSIGNED_COUNT,
            (product_id, contract_partner_id))
        return self.env.cr.fetchone()[0]

    @api.depends('product_id', 'partner_id')
    def _compute_name_address(self):
        """Create subscription name from publication and partner."""
        for this in self:
            if not this.product_id or not this.partner_id:
                this.name = False
                this.display_address = False
                continue
            this.name = ' - '.join(
                [this.product_id.name, this.partner_id.name])
            if this.product_id.distribution_type == 'email':
                this.display_address = this.partner_id.email
            else:
                this.display_address = this.partner_id.contact_address

    @api.multi
    @api.depends('product_id', 'contract_partner_id', 'copies')
    def _compute_counts(self):
        """Used to check how many addresses can still be added."""
        for this in self:
            if not self.product_id or not self.contract_partner_id:
                continue
            contract_count = self.get_product_contract_count(
                this.product_id.id, this.contract_partner_id.id)
            assigned_count = self.get_product_contract_assigned_count(
                this.product_id.id, this.contract_partner_id.id)
            available_count = contract_count - assigned_count
            this.contract_count = contract_count
            this.assigned_count = assigned_count
            this.available_count = available_count

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Publication',
        domain=[('publication', '=', True)],
        required=True)
    distribution_type = fields.Selection(
        string='Type of publication',
        related='product_id.distribution_type',
        store=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Receiving Partner',
        required=True)
    contract_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contract Partner',
        required=True)
    date_start = fields.Date(
        string='Date start',
        default=fields.Date.today(),
        required=True)
    date_end = fields.Date(
        string='Date end')
    copies = fields.Integer(string='Number of copies', default=1)
    name = fields.Char(
        compute='_compute_name_address',
        string='Name')
    display_address = fields.Char(
        compute='_compute_name_address',
        string='Receiving address')
    contract_count = fields.Integer(
        string="Number to distribute",
        compute='_compute_counts')
    assigned_count = fields.Integer(
        string="Number already assigned",
        compute='_compute_counts')
    available_count = fields.Integer(
        string="Number still available",
        compute='_compute_counts')

    @api.onchange('product_id', 'contract_partner_id')
    def _onchange_keyfields(self):
        """Sets the proper domain for contract_partner.

        Also enforces first selecting the publication.
        """
        self.ensure_one()
        if self.contract_partner_id and not self.partner_id:
            self.partner_id = self.contract_partner_id
        if self.contract_partner_id and not self.product_id:
            raise ValidationError(_(
                "You must select a publication, before selecting"
                " the contract partner."))
        if not self.product_id:
            return
        valid_partners = []
        line_model = self.env['account.analytic.invoice.line']
        lines = line_model.search([('product_id', '=', self.product_id.id)])
        for line in lines:
            if line.analytic_account_id.partner_id.id not in valid_partners:
                valid_partners.append(line.analytic_account_id.partner_id.id)
        if not valid_partners:
            raise ValidationError(_(
                "There are no active subscriptions for this publication."))
        partner_domain = [('id', 'in', valid_partners)]
        return {'domain': {'contract_partner_id': partner_domain}}

    @api.model
    def create(self, vals):
        result = super(DistributionList, self).create(vals)
        result._limit_count()
        return result

    @api.multi
    def write(self, vals):
        result = super(DistributionList, self).write(vals)
        self._limit_count()
        return result

    @api.multi
    def _limit_count(self):
        """Limit number of copies send to amount set in contract lines.

        It should be possible to make a constrains method of this function,
        but for inexplicable reasons this does not work.
        """
        for this in self:
            # Do not use counts from 'this' as they probably have not
            # been updated yet.
            product = this.product_id
            contract_partner = this.contract_partner_id
            contract_count = self.get_product_contract_count(
                product.id, contract_partner.id)
            assigned_count = self.get_product_contract_assigned_count(
                product.id, contract_partner.id)
            available_count = contract_count - assigned_count
            if available_count < 0:
                raise ValidationError(_(
                    "Number of copies sent %d can not exceed contracted"
                    " number %d for partner %s and product %s" % (
                        assigned_count,
                        contract_count,
                        contract_partner.display_name,
                        product.display_name)))
