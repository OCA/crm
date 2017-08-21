import logging

import odoo

from .util.odoo_tests import TestBase
from .util.singleton import Singleton

log = logging.getLogger('Test')


class TestMemory(object):
    """Keep records in memory across tests."""
    __metaclass__ = Singleton


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class Test(TestBase):

    def setUp(self):
        super(Test, self).setUp()
        self.memory = TestMemory()

    def test_0001_create_lead(self):

        log.info("""
            - In order to test that the street3 is well passed to the future
            partner, I create a new lead.
        """)

        lead, = self.createAndTest(
            'crm.lead',
            [
                {
                    'name': 'Jester Smurf',
                    'contact_name': 'Jester Smurf',
                    'street': 'Sarsaparilla Street',
                    'street2': 'Cursed Country',
                    'street3': 'Third Mushroom',
                    'city': 'Schtroumpf les Bains',
                    'type': 'lead',
                }
            ],
        )

        log.info("""
            - When I transform the lead in an opportunity,
        """)

        context = {
            'active_model': 'crm.lead',
            'active_id': lead.id,
            'active_ids': [lead.id],
        }

        wizard = (
            self.env['crm.lead2opportunity.partner'].with_context(context).
            create({
                'action': 'create',
                'name': 'convert',
            })
        )

        wizard.action_apply()

        log.info("""
            - then the partner on the opportunity should have the adequate
            street3.
        """)

        self.assertEqual(lead.type, 'opportunity')
        self.assertEqual(lead.partner_id.street3, 'Third Mushroom')
