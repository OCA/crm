# -*- coding: utf-8 -*-
# Copyright 2013 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    resource_ids = fields.Many2many(
        string='Resources',
        comodel_name='resource.resource',
    )
