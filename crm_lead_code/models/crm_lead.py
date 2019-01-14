##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    code = fields.Char(
        string='Lead Number', required=True, default="/", readonly=True)

    _sql_constraints = [
        ('crm_lead_unique_code', 'UNIQUE (code)',
         _('The code must be unique!')),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', '/') == '/':
                vals['code'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return super(CrmLead, self).create(vals_list)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return super(CrmLead, self).copy(default)
