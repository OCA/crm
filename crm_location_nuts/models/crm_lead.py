# -*- coding: utf-8 -*-
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    region = fields.Many2one(comodel_name='res.partner.nuts', string="Region")
    substate = fields.Many2one(comodel_name='res.partner.nuts',
                               string="Substate")

    @api.multi
    def _lead_create_contact(self, name, is_company,
                             parent_id=False):
        """Sets NUTS region on created partner"""
        partner_id = super(CrmLead, self)._lead_create_contact(
            name, is_company, parent_id=parent_id)
        data = {
            'region': self.region,
            'substate': self.substate,
        }
        partner_id.write(data)
        return partner_id
