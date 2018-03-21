# Copyright 2018 brain-tec AG <kumar.aberer@braintec-group.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons.crm.models.crm_lead import CRM_LEAD_FIELDS_TO_MERGE

CRM_LEAD_FIELDS_TO_MERGE.append('industry_id')


class CrmLead(models.Model):
    _inherit = "crm.lead"

    industry_id = fields.Many2one('res.partner.industry',
                                  'Industry')

    @api.model
    def _onchange_partner_id_values(self, partner_id):
        values = super(CrmLead, self)._onchange_partner_id_values(partner_id)

        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            values.update({'industry_id': partner.industry_id.id})

        return values

    @api.multi
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        values = super(CrmLead, self). \
            _create_lead_partner_data(name=name, is_company=is_company,
                                      parent_id=parent_id)
        if self.industry_id:
            values.update({'industry_id': self.industry_id.id})
        return values
