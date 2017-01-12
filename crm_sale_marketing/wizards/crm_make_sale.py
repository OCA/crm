# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class CrmCampaign(models.TransientModel):

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
