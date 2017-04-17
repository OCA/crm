# -*- coding: utf-8 -*-
# Copyright 2013 Savoir-faire Linux
# Copryight 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    resource_ids = fields.Many2many(
        string='Resources',
        comodel_name='resource.resource',
    )

    @api.constrains('resource_ids')
    def _check_resource_ids_dbl_book(self):
        """ Check Double Booking """
        for record in self:

            resources = record.resource_ids.filtered(
                lambda s: s.allow_double_book is False
            )

            if not any(resources):
                continue

            overlaps = self.env['calendar.event'].search([
                ('id', '!=', record.id),
                ('start', '<', record.stop),
                ('stop', '>', record.start),
            ])

            for overlap in overlaps:
                for resource in resources:

                    if resource in overlap.resource_ids:
                        raise ValidationError(_(
                            'The resource, %s, cannot be double-booked '
                            'with any overlapping meetings or events.'
                            % resource.name,
                        ))
