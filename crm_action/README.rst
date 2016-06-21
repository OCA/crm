.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========
CRM Action
==========

This module was written to extend CRM features.
It delivers new object named "Actions" to follow history around leads and opportunities.

Installation
============

Just install the module as usual (it only depends on the native *crm* module).

Configuration
=============

Go to the menu *Sales > Configuration > Leads & Opportunities > Action Types* and create action types.

If you want to have a daily email reminder of your CRM actions to do, go to the menu *Settings > Technical > Automation > Scheduled Actions* and activate the action *CRM Action email reminder* (it is inactive by default). You can customize the email template in the menu *Settings > Technical > Email > Templates* and select the email template named *CRM Action reminder*.

Usage
=====

To use this module, you need to :

1. create a lead or an opportunity,
#. create a new action by using the *Actions* button,
#. when the action is done, click on the button *Mark as done*.

You can overview all actions for any lead or opportunity with the *Actions* menu entry. On the form view of an opportunity, you can see the next action to do and there is also a button to mark it as done (it will immediately display the new next action to do).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/8.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Module developed and tested with Odoo version 8.0

Contributors
------------

* David DUFRESNE <david.dufresne@savoirfairelinux.com>
* Jordi RIERA <jordi.riera@savoirfairelinux.com>
* Bruno JOLIVEAU <bruno.joliveau@savoirfairelinux.com>
* Alexis de Lattre <alexis.delattre@akretion.com>

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
