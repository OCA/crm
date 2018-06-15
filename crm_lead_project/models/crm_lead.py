# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from lxml import etree
from odoo import models, fields, api, _


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    project_id = fields.Many2one('project.project', readonly=True)

    @api.multi
    def action_open_project_form(self):
        return {
            'name': _('Project'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('project.edit_project').id,
            'res_id': self.project_id.id,
            'context': {'remove_create_button': True}
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """Remove create button if view is opened from project action."""
        res = super(CrmLead, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if self.env.context.get('remove_create_button'):
            root = etree.fromstring(res['arch'])
            root.set('create', 'false')
            res['arch'] = etree.tostring(root)
        return res
