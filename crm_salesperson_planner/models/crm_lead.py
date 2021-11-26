# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    crm_salesperson_planner_visit_ids = fields.Many2many(
        comodel_name="crm.salesperson.planner.visit",
        relation="crm_salesperson_planner_visit_crm_lead_rel",
        string="Visits",
        copy=False,
        domain="[('partner_id', 'child_of', partner_id)]",
    )
