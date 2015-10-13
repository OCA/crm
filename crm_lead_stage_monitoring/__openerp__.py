# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2014 Camptocamp SA (http://www.camptocamp.com)
#   @author Vincent Renaville
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

{'name': 'CRM - Add last activity on stage field',
 'version': '1.0.0',
 'category': 'other',
 'description': """This module allow the sale manager to have a quick review of recent stage change on his lead/opportunities.
Each time a lead/opportunity switches from a stage to on other, the Current stage date is updated.
You can make "group by" and search on the Current stage date field 
""",
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'website': 'http://www.camptocamp.com',
 'depends': ['crm'],
 'data': [
          'crm_view.xml'
          ],
 'demo_xml': [],
 'test': [],
 'installable': False,
 'active': False,
 }
