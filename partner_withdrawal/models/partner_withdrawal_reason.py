# -*- encoding: utf-8 -*-
# Copyright 2015 - Antonio Espinosa - Antiun Ingeniería
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class PartnerWithdrawalReason(models.Model):
    _name = 'partner.withdrawal_reason'
    _description = 'Partner membership withdrawal reason'

    name = fields.Char(string="Reason", translate=True, required=True)
