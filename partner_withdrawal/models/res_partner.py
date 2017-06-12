# -*- encoding: utf-8 -*-
# Copyright 2015 - Antonio Espinosa - Antiun Ingeniería
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_signup = fields.Date(string="Signup date")
    membership_withdrawal = fields.Date(string="Withdrawal date")
    membership_withdrawal_reason = fields.Many2one(
        string="Withdrawal reason",
        comodel_name="partner.withdrawal_reason")

    @api.onchange('membership_withdrawal')
    def onchange_membership_withdrawal_reason(self):
        if not self.membership_withdrawal:
            self.membership_withdrawal_reason = False
