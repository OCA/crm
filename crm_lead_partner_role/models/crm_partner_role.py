# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class CrmPartnerRole(models.Model):
    _name = 'crm.partner.role'
    _description = 'Lead partners and roles'

    # Field is called role_partner_id to avoid JS error on opportunity view
    role_partner_id = fields.Many2one('res.partner', string='Partner')

    role_id = fields.Many2one('crm.role', string='Role')

    crm_lead_id = fields.Many2one('crm.lead')
