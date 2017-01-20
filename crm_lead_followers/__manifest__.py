# -*- coding: utf-8 -*-
# © 2017 Leonardo Donelli @ MONK Software <leonardo.donelli@monksoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Share leads with followers',
    'version': '10.0.1.1.0',
    'license': 'AGPL-3',
    'category': 'Sales',
    'author': "MONK Software, Odoo Community Association",
    'summary': "Add users as followers on a lead to share it with them",
    'website': 'http://www.wearemonk.com',
    'depends': ['crm', 'sale_crm'],
    'data': [
        'security/crm_lead_followers_security.xml',
        'security/ir.model.access.csv',
        'views/sales_team.xml',
    ],
    'installable': True,
}
