# -*- coding: utf-8 -*-
##############################################################################
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################

from . import models
from openerp import api, SUPERUSER_ID


def _match_existing_contacts(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID)
        contact_model = env['mail.mass_mailing.contact']
        partner_model = env['res.partner']
        contacts = contact_model.search([])
        for contact in contacts:
            if contact.email:
                partners = partner_model.search([('email', '=ilike',
                                                  contact.email)])
                if partners:
                    contact.write({'partner_id': partners[0].id})
