.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Invoice address in leads
========================

This module was written to extend the functionality of CRM leads to support
setting a separate invoice address.

Usage
=====

To use this module, you need to:

* Go to *Sales > Leads*.
* Open a lead.
* Go to *Extra Info*.
* You will see the new group called *Invoice address*.
* If you uncheck *Use same adress for billing*, you will be able to specify a
  different address for billing purposes.

  The company partner that gets automatically created from that lead will have
  an internal *type* of ``invoice``.

.. image:: https://odoo-community.org/invoice address/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/crm/issues>`_. In
case of trouble, please check there if your issue has already been reported. If
you spotted it first, help us smashing it by providing a detailed and welcomed
feedback `here <https://github.com/OCA/ crm/issues/new?body=module:%20
crm_lead_invoice address%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Rafael Blasco <rafaelbn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
