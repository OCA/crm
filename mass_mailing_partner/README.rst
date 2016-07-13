.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Link partners with mass-mailing
===============================

This module links mass-mailing contacts with partners.

Features
--------
* When creating or saving a mass-mailing contact, partners are matched through
  email, linking matched partner, or creating a new one if no match and the
  maling list partner mandatory field is checked.
* Mailing contacts smart button in partner form.
* Mass mailing stats smart button in partner form.
* Filter and group by partner in mail statistics tree view


Configuration
=============

At first install, all existing mass mailing contacts are matched against
partners. And also mass mailing statistics are matched using model and res_id.

NOTE: When upgrading from version 1.0.0, no mass mailing statistics matching
are done, because it is done only when installing. You can execute 'partner_link'
method to all stats using odoo shell or any XML client:

.. code:: python

    # odoo.py --addons-path=<addons_path_list> shell --config=<odoo_config_file> -d <database>
    stats = self.env['mail.mail.statistics'].search([('model', '!=', False), ('res_id', '!=', False)])
    stats.partner_link()

Usage
=====

In partner view, there is a new action called "Add to mailing list". This
action open a pop-up to select a mailing list. Selected partners will be added
as mailing list contacts.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/8.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/crm/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/crm/issues/new?body=module:%20mass_mailing_partner%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


License
=======

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/agpl-3.0-standalone.html>.


Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Rafael Blasco <rafabn@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>
* Javier Iniesta <javieria@antiun.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
