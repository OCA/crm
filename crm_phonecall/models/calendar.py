# -*- coding: utf-8 -*-
# Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
# Copyright (C) 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    phonecall_id = fields.Many2one(
        comodel_name='crm.phonecall',
        string='Phonecall',
    )
