# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    validate_field_ids = fields.Many2many(
        "ir.model.fields",
        string="Fields to Validate",
        help="Select fields which must be set on the document in this stage",
        domain='[("model", "=", "crm.lead")]',
    )
