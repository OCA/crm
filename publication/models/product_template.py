# -*- coding: utf-8 -*-
# Copyright 2014-2017 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


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
        string='Publish Every',
        default=1,
        help="Publish every (Days/Week/Month/Quarter/Year)")
