# -*- coding: utf-8 -*-
# Copyright 2013 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceResource(models.Model):

    _inherit = 'resource.resource'

    note = fields.Text(
        string='Resource Notes',
    )
    allow_double_book = fields.Boolean(
        string='Allow Double Booking',
        help='Check if this resource '
             'can be booked in more than '
             'one meeting or event at the same '
             'time.',
        default=False,
    )
    event_ids = fields.Many2many(
        string='Calendar Events',
        comodel_name='calendar.event',
    )
