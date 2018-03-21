# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class test_configurator(common.TransactionCase):

    def test_configurator(self):
        placeholders_obj = self.env['email.template.placeholder']
        templates_obj = self.env['email.template']
        invoice_model = self.env['ir.model'].search([
            ('model', '=', 'account.invoice'),
        ])
        placeholders_vals = [
            {
                'name': 'Invoice partner name',
                'model_id': invoice_model.id,
                'placeholder': '${object.partner_id.name}',
            },
            {
                'name': 'Invoice partner vat',
                'model_id': invoice_model.id,
                'placeholder': '${object.partner_id.vat}',
            },
        ]
        for vals in placeholders_vals:
            placeholder = placeholders_obj.create(vals)

            res = templates_obj.onchange({
                'placeholder_id': placeholder.id,
                'placeholder_value': False,
            }, 'placeholder_id', {
                'placeholder_id': 1,
            })['value']
            self.assertEqual(res['placeholder_value'], vals['placeholder'])
