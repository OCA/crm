# -*- coding: utf-8 -*-
# © 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class CrmActionType(models.Model):
    _name = 'crm.action.type'
    _description = 'CRM Action Type'

    name = fields.Char('Name', translate=True, required=True)
    priority = fields.Integer('Priority', required=True, default=0)
    active = fields.Boolean('Active', default=True)

    _order = 'priority'
