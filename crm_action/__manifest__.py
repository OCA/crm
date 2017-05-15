# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'CRM Action',
    'version': '10.0.1.1.0',
    'author': 'Savoir-faire Linux,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Others',
    'summary': 'CRM Action',
    'depends': [
        'sale_crm',
        'sales_team',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/res_groups_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        'views/crm_lead_view.xml',
        'views/crm_action_view.xml',
        'views/crm_action_type_view.xml',
    ],
    'installable': True,
    'application': True,
}
