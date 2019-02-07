# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    ref = fields.Char(string="Reference", readonly=True)

    @api.model
    def _get_next_ref(self):
        return self.env['ir.sequence'].next_by_code('crm.lead')

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            vals['ref'] = self._get_next_ref()
        return super(CrmLead, self).create(values)
