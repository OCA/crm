# Copyright 2018 Savoir-faire Linux
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


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
    allowed_event_types = fields.Many2many(
        string='Event Types',
        comodel_name='calendar.event.type',
        help='Event types this resource is allowed at.',
    )
    calendar_id = fields.Many2one(
        "resource.calendar", string='Working Time',
        default=lambda self: self.env['res.company'].
        _company_default_get().resource_calendar_id,
        required=False,
        help="Define the schedule of resource")
