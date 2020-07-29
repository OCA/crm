# Copyright 2020 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _sync_tag_ids(self):
        """ Synchronizes tag_ids to the sale orders. """
        for rec in self:
            for order in rec.order_ids:
                if order.tag_ids != rec.tag_ids:
                    order.tag_ids = rec.tag_ids

    def write(self, vals):
        res = super().write(vals)
        if 'tag_ids' in vals:
            self._sync_tag_ids()
        return res
