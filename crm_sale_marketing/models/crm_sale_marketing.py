# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class crm_campaign(models.Model):

    _inherit = 'crm.make.sale'

    def makeOrder(self, cr, uid, ids, context=None):
        """
        Sets the marketing data from opportunity when quotation is created
        """
        res = super(crm_campaign, self).makeOrder(cr, uid, ids, context)
        crm_obj = self.pool.get('crm.lead')
        sale_obj = self.pool.get('sale.order')
        sale_id = res.get('res_id')
        crm_id = context.get('active_id')
        crm = crm_obj.browse(cr, uid, crm_id, context)
        sale_obj.write(cr, uid, sale_id,
                       {'campaign_id': crm.campaign_id.id,
                        'medium_id': crm.medium_id.id,
                        'source_id': crm.source_id.id
                        })
        return res
