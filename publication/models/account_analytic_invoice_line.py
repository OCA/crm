# -*- coding: utf-8 -*-
# Copyright 2014-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=no-member,too-few-public-methods
from odoo import api, fields, models


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = 'account.analytic.invoice.line'

    partner_id = fields.Many2one(
        related='analytic_account_id.partner_id',
        store=True,
        readonly=True)
    publication = fields.Boolean(
        string='Subscription product line',
        related='product_id.product_tmpl_id.publication',
        store=True)

    @api.multi
    def action_distribution_list(self):
        self.ensure_one()
        action = self.env.ref(
            'publication.action_distribution_list').read()[0]
        action['context'] = {
            'default_product_id': self.product_id.id,
            'default_contract_partner_id': self.partner_id.id}
        action['domain'] = [
            ('contract_partner_id', '=', self.partner_id.id),
            ('product_id', '=', self.product_id.id)]
        action['view_mode'] = 'form'
        action['target'] = 'current'
        return action

    @api.model
    def create(self, vals):
        this = super(AccountAnalyticInvoiceLine, self).create(vals)
        self.env['distribution.list']._update_contract_partner_copies(
            this.product_id, this.analytic_account_id.partner_id,
        )
        return this

    @api.multi
    def write(self, vals):
        old_values = set(self.mapped(
            lambda x: (x.product_id, x.analytic_account_id.partner_id)
        )) if 'product_id' in vals else []
        result = super(AccountAnalyticInvoiceLine, self).write(vals)
        needs_update = set(['product_id', 'quantity']) & set(vals.keys())
        if needs_update:
            for this in self:
                self.env['distribution.list']._update_contract_partner_copies(
                    this.product_id, this.analytic_account_id.partner_id,
                )
            for product, partner in old_values:
                self.env['distribution.list']._update_contract_partner_copies(
                    product, partner,
                )
        return result

    @api.multi
    def unlink(self):
        updates = set(self.mapped(
            lambda x: (x.product_id, x.analytic_account_id.partner_id)
        ))
        result = super(AccountAnalyticInvoiceLine, self).unlink()
        for product, partner in updates:
            self.env['distribution.list']._update_contract_partner_copies(
                product, partner,
            )
        return result
