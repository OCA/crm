# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re

from odoo import api, fields, models


class PublicationEdition(models.Model):
    """For pdf publications, store the published editions."""
    _name = 'publication.edition'

    @api.depends('name')
    def _pdf_name_get(self):
        # Might be more subtly done with unicodedata and sluggify, but this
        # will cover 99.9% of cases
        if not self.name:
            self.pdf_name = ''
            return
        self.pdf_name = (
            '%s.pdf' % re.sub('[^A-Za-z0-9]+', '-', self.name).lower())

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Publication',
        domain=[('publication', '=', True)],
        required=True)
    date_published = fields.Date(
        string='Date published',
        default=fields.Date.context_today,
        required=True)
    name = fields.Char(
        required=True,
        help="Use name that indicates both publication and edition.\n"
             "For instance: Odoo Times - 2018-02.")
    pdf = fields.Binary(
        string='Pdf',
        required=True,
        copy=False,
        help="Add pdf for publication here")
    pdf_name = fields.Char(
        string='Pdf filename',
        compute=_pdf_name_get)
