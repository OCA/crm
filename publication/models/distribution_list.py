# -*- coding: utf-8 -*-
# Copyright 2014-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=no-member,too-few-public-methods,missing-docstring
# pylint: disable=protected-access,invalid-name
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


SQL_CONTRACT_COUNT = """\
SELECT COALESCE(SUM(ROUND(aail.quantity)::integer), 0) as quantity
 FROM account_analytic_invoice_line aail
 JOIN account_analytic_account aaa
 ON aail.analytic_account_id = aaa.id
 WHERE aail.product_id = %s
   AND aaa.partner_id = %s
   AND (aaa.date_start IS NULL OR DATE(aaa.date_start) <= CURRENT_DATE)
   AND (aaa.date_end IS NULL OR DATE(aaa.date_end) > CURRENT_DATE)
"""

SQL_ASSIGNED_COUNT = """\
SELECT COALESCE(SUM(copies), 0) as copies
 FROM distribution_list
 WHERE product_id = %s
 AND contract_partner_id = %s
"""

DISTRIBUTION_ANALYSIS_STATEMENT = """\
-- Find all combinations of contract partner and publication
-- where not all publications are send in the distribution list
--
-- First select all publication lines
WITH publication_lines AS (
 SELECT
     aaa.partner_id, aail.product_id, pt.default_code,
     COALESCE(SUM(ROUND(aail.quantity)::integer), 0) as quantity
 FROM account_analytic_invoice_line aail
 JOIN account_analytic_account aaa
     ON aail.analytic_account_id = aaa.id
 JOIN product_product pp
     ON aail.product_id = pp.id
 JOIN product_template pt
     ON pp.product_tmpl_id = pt.id
 WHERE pt.publication AND pt.distribution_type = 'print'
   AND (aaa.date_start IS NULL OR DATE(aaa.date_start) <= CURRENT_DATE)
   AND (aaa.date_end IS NULL OR DATE(aaa.date_end) > CURRENT_DATE)
 GROUP BY aaa.partner_id, aail.product_id, pt.default_code
 ),
 -- Then select distribution lines
 distribution_lines AS (
 SELECT
     dl.contract_partner_id, dl.product_id, pt.default_code,
     COALESCE(SUM(ROUND(dl.copies)::integer), 0) as copies
 FROM distribution_list dl
 JOIN product_product pp
     ON dl.product_id = pp.id
 JOIN product_template pt
     ON pp.product_tmpl_id = pt.id
 GROUP BY dl.contract_partner_id, dl.product_id, pt.default_code
 )
 -- Finaly find differences between contracted and distributed copies
 SELECT
     COALESCE(pl.partner_id, dl.contract_partner_id) AS partner_id,
     COALESCE(pl.product_id, dl.product_id) AS product_id,
     COALESCE(pl.default_code, dl.default_code) AS default_code,
     COALESCE(pl.quantity, 0) AS quantity,
     COALESCE(dl.copies, 0) AS copies
 FROM publication_lines pl
 FULL OUTER JOIN distribution_lines dl
     ON pl.partner_id = dl.contract_partner_id
    AND pl.product_id = dl.product_id
 WHERE COALESCE(pl.quantity, 0) <> COALESCE(dl.copies, 0)
"""


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
        partner_model = self.env['res.partner']
        for this in self:
            if not this.product_id or not this.partner_id:
                this.name = False
                this.contact_address = False
                continue
            this.name = ' - '.join(
                [this.product_id.name, this.partner_id.name])
            if this.product_id.distribution_type == 'email':
                this.contact_address = this.partner_id.email
            else:
                delivery_id = this.partner_id.address_get(
                    ['delivery'])['delivery']
                this.contact_address = partner_model.browse(
                    delivery_id).contact_address

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
        related='product_id.product_tmpl_id.distribution_type',
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
    contact_address = fields.Char(
        compute='_compute_name_address',
        string='Receiving address')
    contract_count = fields.Integer(
        string="Quantity to distribute",
        compute='_compute_counts')
    assigned_count = fields.Integer(
        string="Quantity already assigned",
        compute='_compute_counts')
    available_count = fields.Integer(
        string="Quantity still available",
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
                "You must select a publication before selecting"
                " the contract partner."))
        if not self.product_id:
            # If product not yet selected, no limit on partner selection.
            return {'domain': {'contract_partner_id': []}}
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
        self._update_contract_partner_copies(
            result.product_id, result.contract_partner_id,
        )
        return result

    @api.multi
    def write(self, vals):
        old_values = set(self.mapped(
            lambda x: (x.product_id, x.contract_partner_id)
        )) if 'product_id' in vals else []
        result = super(DistributionList, self).write(vals)
        needs_update = set([
            'product_id', 'partner_id', 'contract_partner_id', 'copies'
        ]) & set(vals.keys())
        if needs_update:
            for this in self:
                self._update_contract_partner_copies(
                    this.product_id, this.contract_partner_id,
                )
            for product, partner in old_values:
                self.env['distribution.list']._update_contract_partner_copies(
                    product, partner,
                )
        return result

    @api.multi
    def unlink(self):
        updates = set(self.mapped(
            lambda x: (x.product_id, x.contract_partner_id)
        ))
        result = super(DistributionList, self).unlink()
        for product, partner in updates:
            self._update_contract_partner_copies(product, partner)
        return result

    @api.model
    def _update_contract_partner_copies(self, product, partner):
        """take care that the amount of copies for contract_partner_id partner
        and product is the same as contracted by this partner for the product.
        Balance differences by creating/adjusting a distribution.list entry for
        partner.
        TODO: if we want to support start and end dates, thing get a bit
        trickyer here. Then we need to merge all invoice lines' intervals,
        compartmentalize then to intervals with equal sums of quantities, and
        do the below restricted to every interval but including infinite
        invoice lines and distribution lists
        """
        # ignore mailings (no copies)
        if not product.publication or product.distribution_type != 'print':
            return
        to_assign = self.get_product_contract_count(product.id, partner.id)
        if to_assign == 0:
            # No more (valid) contractlines for contract partner and product.
            to_unlink = self.search([
                ('contract_partner_id', '=', partner.id),
                ('product_id', '=', product.id)])
            super(DistributionList, to_unlink).unlink()
            return
        own = self.search([
            ('contract_partner_id', '=', partner.id),
            ('partner_id', '=', partner.id),
            ('product_id', '=', product.id),
        ])
        others = self.search([
            ('contract_partner_id', '=', partner.id),
            ('partner_id', '!=', partner.id),
            ('product_id', '=', product.id),
        ])
        assign_to_own = to_assign - sum(others.mapped('copies'))
        if assign_to_own < 0:
            raise ValidationError(_(
                "Number of copies sent %d can not exceed contracted"
                " number %d for partner %s and product %s") % (
                    self.get_product_contract_assigned_count(
                        product.id, partner.id,
                    ),
                    to_assign,
                    partner.display_name,
                    product.display_name))
        elif not assign_to_own:
            own.unlink()
        elif not own:
            self.create({
                'product_id': product.id,
                'partner_id': partner.id,
                'contract_partner_id': partner.id,
                'copies': assign_to_own,
            })
        elif len(own) > 1:
            # this unlink will trigger another run of this function where
            # remaining own is updated
            own[1:].unlink()
        elif assign_to_own != own.copies:
            own.write({'copies': assign_to_own})

    @api.model
    def cron_compute_distribution_list(self):
        """Adapt distribution list to contract.

        We use an SQL query to select the records that should be updated.

        For all combinations of parter and publication product that are either
        in contract lines or distribution list entries, we adjust the
        distribution list entry for the contract partner if the number of
        distributed copies is not equal to the number of contracted copies.
        """
        partner_model = self.env['res.partner']
        product_model = self.env['product.product']
        self.env.cr.execute(DISTRIBUTION_ANALYSIS_STATEMENT)
        for row in self.env.cr.fetchall():
            partner = partner_model.browse(row[0])
            product = product_model.browse(row[1])
            self._update_contract_partner_copies(product, partner)
