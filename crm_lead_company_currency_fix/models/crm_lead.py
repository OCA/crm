# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    # OVERRIDE: make ``company_currency`` a stored field
    company_currency = fields.Many2one(store=True)

    def _field_to_sql(self, alias, field_expr, query=None):
        # OVERRIDE: module ``crm`` override for ``field_expr == "company_currency"``
        # creates a SQL object that represents the dynamic nature of the original
        # computed, non-stored field. We need to ignore that to use the DB-stored
        # values instead.
        if field_expr == "company_currency":
            return models.Model._field_to_sql(self, alias, field_expr, query=query)
        return super()._field_to_sql(alias, field_expr, query=query)
