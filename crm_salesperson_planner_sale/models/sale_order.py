# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    visit_id = fields.Many2one(
        comodel_name="crm.salesperson.planner.visit",
        string="Visit",
        check_company=True,
        domain="[('partner_id', 'child_of', partner_id),"
        " '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
