# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# © 2016 Antonio Espinosa - <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Link partners with mass-mailing",
    "version": "8.0.2.0.0",
    "author": "Tecnativa, "
              "Antiun Ingeniería S.L., "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Marketing",
    "depends": [
        'mass_mailing',
    ],
    "post_init_hook": "post_init_hook",
    'data': [
        'views/mail_mail_statistics_view.xml',
        'views/mail_mass_mailing_contact_view.xml',
        'views/mail_mass_mailing_view.xml',
        'views/res_partner_view.xml',
        'wizard/partner_mail_list_wizard.xml'
    ],
    "installable": True,
}
