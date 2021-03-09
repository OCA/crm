# Copyright 2020 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br> - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    secondary_user_id = fields.Many2one(
        comodel_name="res.users", string="Secondary Salesperson", tracking=True
    )

    _sql_constraints = [
        (
            "secondary_user_id",
            "CHECK((secondary_user_id IS NULL) OR (secondary_user_id != user_id))",
            "The secondary salesperson must be different from the primary salesperson!",
        ),
    ]
