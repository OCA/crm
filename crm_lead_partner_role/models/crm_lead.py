# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    partner_role_ids = fields.One2many(
        'crm.partner.role',
        inverse_name='crm_lead_id',
        help='Partners involved on this lead and their roles.'
    )
