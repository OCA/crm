# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Vauxoo
#    Author : Yanina Aular <yani@vauxoo.com>
#             Osval Reyes <osval@vauxoo.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': 'CRM Claim Types',
    'category': 'Customer Relationship Management',
    'summary': 'Claim types for CRM',
    'author': 'Odoo Community Association (OCA),'
              'Vauxoo',
    'website': 'https://www.vauxoo.com/',
    'license': 'AGPL-3',
    'version': '8.0.1.0.0',
    'depends': [
        'crm_claim',
    ],
    'data': [
        'data/crm_claim_type.xml',
        'data/crm_claim_stage.xml',
        'security/ir.model.access.csv',
        'views/crm_claim.xml',
        'views/crm_claim_stage.xml',
        'views/crm_claim_type.xml',
    ],
    'demo': [
        'demo/crm_claim.xml',
        'demo/crm_claim_stage.xml',
    ],
    'installable': True,
    'auto_install': False,
}
