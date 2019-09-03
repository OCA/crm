# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class CrmLead(models.Model):
    """Add third field in lead address"""

    _inherit = "crm.lead"

    @api.multi
    def _lead_create_contact(self, name, is_company, parent_id=False):

        partner = super(CrmLead, self)._lead_create_contact(
            name, is_company, parent_id=parent_id,
        )

        partner.write({'street3': self.street3})

        return partner

    street3 = fields.Char('Street 3')

    def _onchange_partner_id_values(self, partner_id):

        res = super(CrmLead, self)._onchange_partner_id_values(partner_id)

        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            res.update({'street3': partner.street3})

        return res
