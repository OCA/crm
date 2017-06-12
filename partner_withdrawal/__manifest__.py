# -*- encoding: utf-8 -*-
# Copyright 2015 - Antonio Espinosa - Antiun Ingeniería
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': "Partner membership withdrawal",
    'category': 'Association',
    'version': '10.0.1.0.0',
    'depends': [
        'sales_team',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/partner_withdrawal_reason_view.xml',
        'security/ir.model.access.csv',
    ],
    'author': 'Antiun Ingeniería, Odoo Community Association (OCA)',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
