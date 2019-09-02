# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class CrmRole(models.Model):

    _name = 'crm.role'
    _description = 'CRM Role'

    name = fields.Char(required=True)
