# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    recipient_res_registry_ids = fields.One2many(
        comodel_name='res.registry',
        inverse_name='recipient_partner_id',
        string='Registry as recipient',
    )

    number_of_registers_as_recipent = fields.Integer(
        string='Num. registers as recipient',
        compute='_compute_number_of_registers_as_recipent',
        store=True,
    )

    sender_res_registry_ids = fields.One2many(
        comodel_name='res.registry',
        inverse_name='sender_partner_id',
        string='Registry as sender',
    )

    number_of_registers_as_sender = fields.Integer(
        string='Num. registers as sender',
        compute='_compute_number_of_registers_as_sender',
        store=True,
    )

    total_res_registry_ids = fields.One2many(
        comodel_name='res.registry',
        compute='_compute_total_res_registry_ids',
        string='Registry',
    )

    number_of_total_registers = fields.Integer(
        string='Num. registers',
        compute='_compute_number_of_total_registers',
        store=True,
    )

    @api.depends('recipient_res_registry_ids')
    def _compute_number_of_registers_as_recipent(self):
        for record in self:
            record.number_of_registers_as_recipent = \
                len(record.recipient_res_registry_ids)

    @api.depends('sender_res_registry_ids')
    def _compute_number_of_registers_as_sender(self):
        for record in self:
            record.number_of_registers_as_sender = \
                len(record.sender_res_registry_ids)

    @api.depends('total_res_registry_ids')
    def _compute_number_of_total_registers(self):
        for record in self:
            record.number_of_total_registers = \
                len(record.total_res_registry_ids)

    @api.depends('recipient_res_registry_ids', 'sender_res_registry_ids')
    def _compute_total_res_registry_ids(self):
        for record in self:
            record.total_res_registry_ids = \
                (record.recipient_res_registry_ids |
                    record.sender_res_registry_ids)

    def action_get_registers(self):
        self.ensure_one()
        tree_view = \
            self.env.ref('crm_registrymgmt.res_registry_tree_view').id
        form_view = \
            self.env.ref('crm_registrymgmt.res_registry_form_view').id
        search_view = \
            self.env.ref('crm_registrymgmt.res_registry_search_view').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Registers'),
            'res_model': 'res.registry',
            'view_mode': 'tree,form',
            'views': [(tree_view, 'tree'), (form_view, 'form')],
            'search_view_id': search_view,
            'target': 'current',
            'domain': [('id', 'in', self.total_res_registry_ids.ids)],
        }

    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )

        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//button[@name='action_get_registers']"):
                node.set(
                    'modifiers',
                    '{"invisible": [["number_of_total_registers", "=", 0]]}'
                )
            res['arch'] = etree.tostring(doc, encoding='unicode')

        return res
