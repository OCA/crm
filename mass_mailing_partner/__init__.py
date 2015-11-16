# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from . import models
from . import wizard
from openerp import api, SUPERUSER_ID


def _match_existing_contacts(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        contact_model = env['mail.mass_mailing.contact']
        partner_model = env['res.partner']
        contacts = contact_model.search([('email', '!=', False)])
        for contact in contacts:
            if contact.email:
                partners = partner_model.search([('email', '=ilike',
                                                  contact.email)])
                if partners:
                    contact.write({'partner_id': partners[0].id})
