# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
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
    'name': 'Calendar Resources',
    'version': '8.0.1.0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'CRM',
    'summary': 'New features to facilitate resources management with meetings',
    'description': """
CRM Meeting Resources
=====================
This module add new features to facilitate your resources management with your meetings :
- improvement in resource.resource native object (image, note and boolean choice for using it in your calendars)
- add a link between your calendars and your resources,
- switch easily your calendar's views with attendees and resources,
- add a new menu entry to display event by resources in several views (calendar, list and form)

Note that the customer don't expect for this step :
- any constraint between resources reservations in calendar,
- any interface with calendar_google for the 'resource' object.

Contributors
------------

    Jordi RIERA (jordi.riera@savoirfairelinux.com)
    Bruno JOLIVEAU (bruno.joliveau@savoirfairelinux.com)

More information
----------------
* Module developed and tested with Odoo version 8.0
* For questions, please contact our support services \
(support@savoirfairelinux.com)
""",
    'depends': [
        'resource',
        'calendar',
    ],
    'data': [
        'views/resource_view.xml',
    ],
    'installable': True,
}
