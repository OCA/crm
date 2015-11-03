# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
    'name': 'Mass Mailing Keep Archives',
    'version': '8.0.0.0.0',
    'description': """
Mass Mailing Keep Archives
==========================
This module adds an option on mass mailing campaings to allow you set if you
want to keep archives (mails sent) or not.
""",
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'depends': [
        'mass_mailing',
        ],
    'data': [
        'mass_mailing_view.xml',
        ],
    'demo': [
        ],
    'test': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
