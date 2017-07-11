# -*- coding: utf-8 -*-
# Copyright 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CalendarEventType(models.Model):

    _inherit = 'calendar.event.type'

    allowed_resource_ids = fields.Many2many(
        string='Allowed Resources',
        comodel_name='resource.resource',
        help='Resources allowed in meetings of this type',
    )
