# -*- coding: utf-8 -*-
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
# ############ Credits ########################################################
#    Coded by: Yanina Aular <yani@vauxoo.com>
#    Planified by: Yanina Aular <yani@vauxoo.com>
#    Audited by: Moises Lopez <moylop260@vauxoo.com>
#                Nhomar Hernandez <nhomar@vauxoo.com>
# ##############################################################################
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
# ##############################################################################
{
    'name': 'CRM Claim Types',
    'category': 'Customer Relationship Management',
    'summary': 'Claim types for CRM',
    'author': 'Odoo Community Association (OCA),'
              'Vauxoo',
    'website': 'www.vauxoo.com',
    'version': '1.0',
    'depends': [
        'crm_claim',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_claim_type_view.xml',
        'views/crm_case_claims_form_view.xml',
        'data/crm_claim_type_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
