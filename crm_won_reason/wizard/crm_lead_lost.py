# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import fields, models


class CrmLeadLost(models.TransientModel):
    _inherit = "crm.lead.lost"

    lost_reason_id = fields.Many2one(domain="[('reason_type', 'in', (False, 'lost'))]")
