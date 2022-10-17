# Copyright 2022 Telmo Santos <telmo.santos@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    opportunity_id = fields.Many2one(
        "crm.lead",
        string="Opportunity",
        check_company=True,
        domain="[('type', '=', 'opportunity'), ('request_type', '=', 'supplier'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",  # noqa
    )
