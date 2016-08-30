# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class CrmCampaign(models.Model):

    _inherit = 'crm.make.sale'

    @api.multi
    def makeOrder(self):
        """
        Sets the marketing data from opportunity when quotation is created
        """
        res = super(CrmCampaign, self).makeOrder()
        crm_obj = self.env['crm.lead']
        sale_obj = self.env['sale.order']
        sale_id = res.get('res_id')
        sale = sale_obj.browse(sale_id)
        crm_id = self._context.get('active_id')
        crm = crm_obj.browse(crm_id)
        sale.write({'campaign_id': crm.campaign_id.id,
                    'medium_id': crm.medium_id.id,
                    'source_id': crm.source_id.id})
        return res
