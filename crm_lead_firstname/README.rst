.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Firstname and Lastname in Leads
===============================

This module extends the functionality of CRM leads to support split first and
last name fields for contacts and allow you to port that information to and
from partners.


Installation
============

Since leads are expected to create partners only when needed and after
information is correctly set up, in leads there is no inverse logic to
transform the old single name in the new split names automatically. The old
single name will simply be the firstname now.

To install this module, you need to:

* Install `OCA/partner-contact <https://github.com/OCA/partner-contact>`_ repo.

Usage
=====

To use this module, you need to:

* Go to *Sales > Sales > Leads > Create*.
* You have the new split fields *Firstname* and *Lastname*. Fill them.
* Press *Convert to Opportunity*.
* In *Related Customer* choose *Create a new customer*.
* Press *Create Opportunity*.
* In the new opportunity, go to *Lead* tab. There are the new fields too.
* If you go to the partner you just created, you will see that its first and
  last names match those in the lead.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
crm/issues/new?body=module:%20
crm_lead_firstname%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
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

To contribute to this module, please visit https://odoo-community.org.
