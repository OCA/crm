from odoo import fields, models


class Tag(models.Model):
    _inherit = [
        'crm.tag',
    ]

    sales_team_ids = fields.Many2many('crm.team', string='Teams',)
