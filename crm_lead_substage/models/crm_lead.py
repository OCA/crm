# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    substage_id = fields.Many2one(
        comodel_name="crm.case.substage", string="Substage",
        domain="[('stage_id', '=', stage_id)]")

    @api.multi
    def onchange_stage_id(self, stage_id):
        res = super(CrmLead, self).onchange_stage_id(stage_id)
        res['value'] = res.get('value', {})
        res['value']['substage_id'] = False
        return res
