# -*- coding: utf-8 -*-
# © 2015 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Crm Auto Alias',
    'summary': 'Automatically generates an email alias related to lead',
    'version': '8.0.1.0.0',
    'author': "FactorLibre,Odoo Community Association (OCA)",
    'category': 'Customer Relationship Management',
    'depends': ['crm', 'mail'],
    'website': 'http://factorlibre.com',
    'data': [
        'view/crm_lead_view.xml'
    ],
    'test': ['test/test_autoalias.yml'],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'post_init_hook': 'assign_alias_to_crm'
}
