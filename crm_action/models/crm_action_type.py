# -*- coding: utf-8 -*-
# Copyright Savoir-faire Linux, Equitania Software GmbH, Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class CrmActionType(models.Model):
    _name = 'crm.action.type'
    _description = 'CRM Action Type'

    name = fields.Char('Name', translate=True, required=True)
    priority = fields.Integer('Priority', required=True, default=0)
    is_active = fields.Boolean('Active', default=True)

    _order = 'priority'
