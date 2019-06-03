# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Mailchimp integration",
    "version": "10.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Marketing",
    "summary": "Manage your mailchimp audiences with Odoo",
    "depends": [
        'mail',
    ],
    "demo": [
        "demo/mailchimp_list.xml",
        "demo/mailchimp_interest_category.xml",
        "demo/mailchimp_interest.xml",
        "demo/res_partner.xml",
        "demo/res_users.xml",
    ],
    "data": [
        "data/ir_cron.xml",
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "views/res_partner.xml",
        "views/mailchimp_interest_category.xml",
        "views/mailchimp_merge_field.xml",
        "views/mailchimp_settings.xml",
        "views/mailchimp_list.xml",
        "views/menu.xml",
        'security/ir.model.access.csv',
    ],
    "external_dependencies": {
        'python': ['mailchimp3'],
    },
}
