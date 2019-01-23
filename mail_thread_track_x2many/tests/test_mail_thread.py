# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase
from openerp import registry


class TestMailThread(TransactionCase):

    at_install = True

    def setUp(self):
        super(TestMailThread, self).setUp()
        res_partner = self.env['res.partner']
        res_partner_category = self.env['res.partner.category']
        self.partner1 = res_partner.create({'name': 'test'})
        self.partner2 = res_partner.create({'name': 'test2'})
        self.partner3 = res_partner.create({'name': 'test3'})
        self.categ1 = res_partner_category.create({'name': 'categ1'})
        self.categ2 = res_partner_category.create({'name': 'categ2'})

    def test_add_records(self):
        self.partner1.child_ids.track_visibility = 'onchange'
        self.partner1.category_id.track_visibility = 'onchange'
        module = self.env['ir.module.module'].search([
            ('name', '=', 'mail_thread_track_x2many')])
        #from openerp.modules.registry import RegistryManager
        from openerp.modules.module import load_openerp_module
        load_openerp_module('mail_thread_track_x2many')
        self.partner1.write({
            'child_ids': [(6, False, self.partner2.ids + self.partner3.ids)],
            'category_id': [(6, False, self.categ1.ids + self.categ2.ids)],
        })

    def test_delete_records(self):
        pass

    def test_edit_records(self):
        pass
