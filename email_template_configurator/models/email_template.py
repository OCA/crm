# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class EmailTemplate(models.Model):

    _inherit = 'email.template'

    # Fake field for auto-completing placeholder
    placeholder_id = fields.Many2one(
        'email.template.placeholder', string="Placeholder")
    placeholder_value = fields.Char()

    @api.onchange('placeholder_id')
    def _onchange_placeholder_id(self):
        for tmpl in self:
            if tmpl.placeholder_id:
                tmpl.placeholder_value = tmpl.placeholder_id.placeholder
                tmpl.placeholder_id = False
