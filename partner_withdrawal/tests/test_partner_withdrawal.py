# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0

from odoo.tests import common
from odoo import fields
from datetime import timedelta, datetime


class TestPartnerWithdrawal(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerWithdrawal, cls).setUpClass()
        date_time = fields.Datetime.to_string(
            datetime.now() - timedelta(hours=1))
        cls.reason = cls.env['partner.withdrawal_reason'].create({
            'name': 'Test reason',
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test name',
            'membership_signup': date_time,
            'membership_withdrawal': date_time,
            'membership_withdrawal_reason': cls.reason.id,
        })

    def test_onchange_membership_withdrawal_reason(self):
        self.partner.membership_withdrawal = False
        self.partner.onchange_membership_withdrawal_reason()
        self.assertEqual(self.partner.membership_withdrawal_reason.id, False)
