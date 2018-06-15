# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from lxml import etree
from odoo import models, fields, api, _


class ProjectProject(models.Model):

    _inherit = 'project.project'

    crm_project = fields.Boolean(readonly=True)
    lead_id = fields.Many2one('crm.lead', readonly=True)

    @api.multi
    def action_open_opportunity_form(self):
        return {
            'name': _('Opportunity'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('crm.crm_case_form_view_oppor').id,
            'res_id': self.lead_id.id,
            'context': {'remove_create_button': True}
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """Remove create button if view is opened from opportunity action."""
        res = super(ProjectProject, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if self.env.context.get('remove_create_button'):
            root = etree.fromstring(res['arch'])
            root.set('create', 'false')
            res['arch'] = etree.tostring(root)
        return res
