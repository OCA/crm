# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api


class CrmOpportunityCreateProject(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner'
    _name = 'crm.opportunity.create.project'

    @api.multi
    def action_create_project(self):
        self.ensure_one()
        leads = self.env['crm.lead'].browse(
            self.env.context.get('active_ids', []))
        self.create_projects(leads)
        return leads.redirect_opportunity_view()
