# -*- coding: utf-8 -*-
# Copyright 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class CrmActionType(models.Model):
    _name = 'crm.action.type'
    _description = 'CRM Action Type'

    name = fields.Char(
        string='Name',
        translate=True,
        required=True,
    )
    priority = fields.Integer(
        string='Priority',
        required=True, default=0,
    )
    active = fields.Boolean(
        default=True,
    )

    _order = 'priority'
