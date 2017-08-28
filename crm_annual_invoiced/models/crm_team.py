# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models, _


class CrmTeam(models.Model):
    _inherit = "crm.team"

    forecast_period = fields.Selection([
                ('monthly', _('Monthly')),
                ('annual', _('Annual')),
            ],
            string='Forecast period',
            default='monthly')
    annual_invoiced = fields.Integer(
            compute="_compute_annual_invoiced",
            readonly=True,
            string='Invoiced this year',
            help="Invoice revenue for the current year. This is the amount "
                    "the sales team has invoiced this month. "
                    "It is used to compute the progression ratio "
                    "of the current and target revenue on the kanban view.")

    @api.multi
    def _compute_annual_invoiced(self):
        date_begin = date.today().replace(day=1, month=1)
        date_end = date(date.today().year, 12, 31)

        for team in self:
            invoices = self.env['account.invoice'].search([
                ('state', 'in', ['open', 'paid']),
                ('team_id', '=', team.id),
                ('date', '<=', date_end),
                ('date', '>=', date_begin),
                ('type', 'in', ['out_invoice', 'out_refund']),
            ])

            team.annual_invoiced = sum(
                invoices.mapped('amount_untaxed_signed'))
