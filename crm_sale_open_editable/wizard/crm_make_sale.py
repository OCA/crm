# -*- coding: utf-8 -*-
# (c) 2016 credativ ltd. - Ondřej Kuzník
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class CRMMakeSale(models.TransientModel):
    _name = "crm.make.sale"

    @api.model
    def makeOrder(self, ids):
        res = super(CRMMakeSale, self).makeOrder(ids)
        if res.get('type') == 'ir.actions.act_window':
            res.setdefault('flags', {}).update(
                {'form': {'options': {'mode': 'edit'}}})

        return res
