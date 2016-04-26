# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

{
    "name": "Link partners with mass-mailing",
    "version": "8.0.1.0.0",
    "author": "Antiun Ingeniería S.L., "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Marketing",
    "depends": [
        'mass_mailing',
    ],
    "post_init_hook": "_match_existing_contacts",
    'data': [
        'views/mail_mass_mailing_contact_view.xml',
        'views/mail_mass_mailing_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
