# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common
from openerp import fields


class TestLetterManagement(common.TransactionCase):

    def setUp(self):
        super(TestLetterManagement, self).setUp()
        self.partner1 = self.env['res.partner'].create({
            'name': 'Dummy Partner #1',
        })

    def test_letter_out(self):
        letter = self.env['res.letter'].with_context(move='out').create({
            'recipient_partner_id': self.partner1.id
        })

        self.assertTrue(bool(letter.number))
        self.assertEqual(letter.date, fields.Date.today())
        self.assertEqual(letter.move, 'out')

        self.assertEqual(
            letter.sender_partner_id,
            self.env.user.company_id.partner_id,
            'Default sender should be current user company')

        letter.action_send()
        self.assertEqual(letter.state, 'sent')
        self.assertEqual(letter.snd_date, fields.Date.today())

        letter.action_received()
        self.assertEqual(letter.state, 'rec')
        self.assertEqual(letter.rec_date, fields.Date.today())

        letter.action_rec_ret()
        self.assertEqual(letter.state, 'rec_ret')
        letter.action_rec_bad()
        self.assertEqual(letter.state, 'rec_bad')

        letter.action_cancel()
        self.assertEqual(letter.state, 'cancel')

        letter.action_cancel_draft()
        self.assertEqual(letter.state, 'draft')

    def test_letter_in(self):
        letter = self.env['res.letter'].with_context(move='in').create({
            'sender_partner_id': self.partner1.id
        })

        self.assertEqual(letter.move, 'in')
        self.assertEqual(
            letter.recipient_partner_id,
            self.env.user.company_id.partner_id,
            'Default recipient should be current user company')
