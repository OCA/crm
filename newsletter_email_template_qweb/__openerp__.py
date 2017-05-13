# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "QWeb expressions in newsletters",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Newsletter",
    "summary": "Glue module for newsletter and email_template_qweb",
    "depends": [
        'newsletter',
        'email_template_qweb',
    ],
    "data": [
        "views/newsletter_newsletter.xml",
        "views/templates.xml",
    ],
    "auto_install": True,
    "installable": True,
}
