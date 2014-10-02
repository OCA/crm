# -*- coding: utf-8 -*-
# Copyright 2014-2017 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    subscription_ids = fields.One2many(
        comodel_name='account.analytic.invoice.line',
        inverse_name='partner_id',
        domain=[('publication', '=', True)],
        string='Subscription contract lines')

    distribution_list_ids = fields.One2many(
        comodel_name='distribution.list',
        inverse_name='partner_id',
        string='Publications received')
