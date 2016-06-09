# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.tools.safe_eval import safe_eval


class TestDeduplicateByFuzzyName(common.TransactionCase):
    def setUp(self):
        super(TestDeduplicateByFuzzyName, self).setUp()
        self.partner_1 = self.env['res.partner'].create({
            'name': 'Partner',
            'email': 'somebody@somewhere.com',
        })
        self.partner_2 = self.env['res.partner'].create({
            'name': 'Portner',
        })
        self.partner_3 = self.env['res.partner'].create({
            'name': 'Poltner',
        })
        self.wizard = self.env['base.partner.merge.automatic.wizard'].create({
            'fuzzy_name_group_by': True,
            'max_fuzzy_name_difference': 1,
        })

    def test_deduplicate_by_fuzzy_name_match(self):
        self.wizard.start_process_cb()
        found_match = False
        for line in self.wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if (self.partner_1.id in match_ids and
                    self.partner_2.id in match_ids and
                    len(match_ids) == 2):
                found_match = True
                break
        self.assertTrue(found_match)

    def test_deduplicate_by_fuzzy_name_no_match(self):
        self.wizard.max_fuzzy_name_difference = 2
        self.wizard.start_process_cb()
        found_match = False
        for line in self.wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if (self.partner_1.id in match_ids and
                    self.partner_2.id in match_ids and
                    len(match_ids) == 2):
                found_match = True
                break
        self.assertFalse(found_match)

    def test_deduplicate_by_fuzzy_name_with_other_criteria(self):
        self.wizard.group_by_email = True
        self.wizard.start_process_cb()
        found_match = False
        for line in self.wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if (self.partner_1.id in match_ids and
                    self.partner_2.id in match_ids and
                    len(match_ids) == 2):
                found_match = True
                break
        self.assertFalse(found_match)
