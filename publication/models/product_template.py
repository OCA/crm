# -*- coding: utf-8 -*-
# Copyright 2014-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    publication = fields.Boolean(string='Product is a publication?')
    distribution_type = fields.Selection(
        selection=[('email', 'Electronic'), ('print', 'Print')],
        string='Distribution',
        help="Required if product is  publication")
    publishing_frequency_type = fields.Selection(
        selection=[
            ('irregular', 'Irregular'),
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Year(s)')],
        default='monthly',
        string='Publishing frequency',
        help="At what intervals publication is published")
    publishing_frequency_interval = fields.Integer(
        string='Published Every',
        default=1,
        help="Published every (Days/Week/Month/Quarter/Year)")

    @api.multi
    def action_distribution_list(self):
        self.ensure_one()
        action = self.env.ref(
            'publication.action_distribution_list').read()[0]
        action['context'] = {
            'default_product_id': self.product_variant_ids[0].id}
        action['domain'] = [
            ('product_id', '=', self.product_variant_ids[0].id)]
        action['view_mode'] = 'form'
        action['target'] = 'current'
        return action
