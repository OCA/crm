# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestPublication(common.SavepointCase):

    post_install = True
    at_install = False

    @classmethod
    def setUpClass(cls):
        super(TestPublication, cls).setUpClass()
        # Create some test partners
        partner_model = cls.env['res.partner']
        cls.partner_jan = partner_jan = partner_model.create({
            'name': 'Jan',
            'city': 'Amsterdam'})
        cls.partner_piet = partner_piet = partner_model.create({
            'name': 'Piet',
            'city': 'Rotterdam'})
        cls.partner_joris = partner_model.create({
            'name': 'Joris',
            'city': 'Den Haag'})
        cls.partner_corneel = partner_model.create({
            'name': 'Corneel',
            'city': 'Dordrecht'})
        # Make sure a sale journal is present for tests
        sequence_model = cls.env['ir.sequence']
        contract_sequence = sequence_model.create({
            'company_id': cls.env.user.company_id.id,
            'code': 'contract',
            'name': 'contract sequence',
            'number_next': 1,
            'implementation': 'standard',
            'padding': 3,
            'number_increment': 1})
        journal_model = cls.env['account.journal']
        journal_model.create({
            'company_id': cls.env.user.company_id.id,
            'code': 'contract',
            'name': 'contract journal',
            'sequence_id': contract_sequence.id,
            'type': 'sale'})
        # Create products:
        cls.uom_unit = cls.env.ref('product.product_uom_unit')
        product_model = cls.env['product.product']
        cls.product_book = product_book = product_model.create({
            'name': 'Test yearbook',
            'type': 'product',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id})
        cls.product_newsletter = product_newsletter = product_model.create({
            'name': 'Test newsletter',
            'type': 'consu',
            'publication': True,
            'distribution_type': 'email',
            'publishing_frequency_type': 'weekly',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id})
        # Create contract that will be subscription from the beginning:
        contract_model = cls.env['account.analytic.account']
        line_model = cls.env['account.analytic.invoice.line']
        cls.contract_jan = contract_jan = contract_model.create({
            'name': 'Test Contract Jan',
            'partner_id': partner_jan.id,
            'pricelist_id': partner_jan.property_product_pricelist.id,
            'recurring_invoices': True,
            'date_start': '2016-02-15',
            'recurring_next_date': '2016-02-29'})
        cls.line_newsletter = line_model.create({
            'analytic_account_id': contract_jan.id,
            'product_id': product_newsletter.id,
            'name': 'Newsletter subscription',
            'quantity': 40,
            'uom_id': product_newsletter.uom_id.id,
            'price_unit': 100,
            'discount': 50})
        # Create contract for yearbook. product will be changed to publication:
        cls.contract_piet = contract_piet = contract_model.create({
            'name': 'Test Contract Piet',
            'partner_id': partner_piet.id,
            'pricelist_id': partner_piet.property_product_pricelist.id,
            'recurring_invoices': True,
            'date_start': '2016-02-15',
            'recurring_next_date': '2016-02-29'})
        cls.line_book = line_model.create({
            'analytic_account_id': contract_piet.id,
            'product_id': product_book.id,
            'name': 'Newsletter subscription',
            'quantity': 1,
            'uom_id': product_book.uom_id.id,
            'price_unit': 100,
            'discount': 50})

    def test_contract(self):
        """Test creation of contract line for publication."""
        line_newsletter = self.line_newsletter
        partner_jan = self.partner_jan
        self.assertTrue(line_newsletter.publication)
        self.assertEqual(partner_jan.subscription_ids[0], line_newsletter)

    def test_product_change(self):
        """Test change of product to publication product."""
        product_book = self.product_book
        line_book = self.line_book
        partner_piet = self.partner_piet
        self.assertFalse(line_book.publication)
        self.assertFalse(bool(partner_piet.subscription_ids))
        product_book.write({
            'publication': True,
            'distribution_type': 'print',
            'publishing_frequency_type': 'yearly'})
        self.assertTrue(line_book.publication)
        self.assertEqual(partner_piet.subscription_ids[0], line_book)

    def test_distribution_list(self):
        """Test adding recipients to distribution list."""
        distribution_model = self.env['distribution.list']
        product_newsletter = self.product_newsletter
        partner_jan = self.partner_jan
        partner_joris = self.partner_joris
        partner_corneel = self.partner_corneel
        product_count = distribution_model.get_product_contract_count(
            product_newsletter.id, partner_jan.id)
        self.assertEqual(product_count, 40)
        assigned_count = \
            distribution_model.get_product_contract_assigned_count(
                product_newsletter.id, partner_jan.id)
        self.assertEqual(assigned_count, 0)
        subscription01 = distribution_model.create({
            'product_id': product_newsletter.id,
            'contract_partner_id': partner_jan.id,
            'partner_id': partner_joris.id,
            'copies': 10})
        self.assertEqual(subscription01.contract_count, 40)
        self.assertEqual(subscription01.assigned_count, 10)
        self.assertEqual(subscription01.available_count, 30)
        subscription02 = distribution_model.create({
            'product_id': product_newsletter.id,
            'contract_partner_id': partner_jan.id,
            'partner_id': partner_corneel.id,
            'copies': 10})
        self.assertEqual(subscription02.contract_count, 40)
        # Old entry should also be changed
        self.assertEqual(subscription01.assigned_count, 20)
        self.assertEqual(subscription01.available_count, 20)
        with self.assertRaises(ValidationError):
            distribution_model.create({
                'product_id': product_newsletter.id,
                'contract_partner_id': partner_jan.id,
                'partner_id': partner_jan.id,
                'copies': 30})
