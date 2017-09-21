# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class Test(TransactionCase):

    def setUp(self):

        super(Test, self).setUp()

        # In order to test that the street3 is well passed to the future
        # partner, I create a new lead.
        self.lead = self.env['crm.lead'].create({
            'name': 'Jester Smurf',
            'contact_name': 'Jester Smurf',
            'street': 'Sarsaparilla Street',
            'street2': 'Cursed Country',
            'street3': 'Third Mushroom',
            'city': 'Schtroumpf les Bains',
            'type': 'lead',
        })

    def test_transform_lead(self):

        # When I transform the lead in an opportunity,

        context = {
            'active_model': 'crm.lead',
            'active_id': self.lead.id,
            'active_ids': [self.lead.id],
        }

        wizard = (
            self.env['crm.lead2opportunity.partner'].with_context(context).
            create({
                'action': 'create',
                'name': 'convert',
            })
        )

        wizard.action_apply()

        # then the partner on the opportunity should have the adequate street3.

        self.assertEqual(self.lead.type, 'opportunity')
        self.assertEqual(self.lead.partner_id.street3, 'Third Mushroom')
