# Copyright 2020 Adgensee - Vincent Garcies
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    lead_id = fields.Many2one("crm.lead", string="Opportunity")
