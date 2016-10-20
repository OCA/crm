# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    code = fields.Char(
        string='Lead Number', required=True, default="/", readonly=True)

    _sql_constraints = [
        ('crm_lead_unique_code', 'UNIQUE (code)',
         'The code must be unique!'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].get('crm.lead')
        return super(CrmLead, self).create(vals)

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].get('crm.lead')
        return super(CrmLead, self).copy(default)
