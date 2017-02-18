# -*- coding: utf-8 -*-
# Copyright 2013 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceResource(models.Model):

    _inherit = 'resource.resource'

    note = fields.Text(
        string='Resource Notes',
    )
