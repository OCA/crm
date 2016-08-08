# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# © 2016 Antonio Espinosa - <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # ACTION 1: Match existing contacts
        contact_model = env['mail.mass_mailing.contact']
        partner_model = env['res.partner']
        contacts = contact_model.search([('email', '!=', False)])
        _logger.info('Trying to match %d contacts to partner by email',
                     len(contacts))
        for contact in contacts:
            partners = partner_model.search([
                ('email', '=ilike', contact.email)
            ], limit=1)
            if partners:
                contact.write({'partner_id': partners.id})
        # ACTION 2: Match existing statistics
        stat_model = env['mail.mail.statistics']
        stats = stat_model.search([
            ('model', '!=', False),
            ('res_id', '!=', False),
        ])
        _logger.info('Trying to link %d mass mailing statistics to partner',
                     len(stats))
        stats.partner_link()
