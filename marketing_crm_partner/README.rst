.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Tracking Fields in Partners
===========================

This module extends the functionality of the CRM to support having the tracking
fields available in the partner and copy them there automatically when the
partner is created from a lead/opportunity.

Configuration
=============

To configure this module, you need to:

* Go to *Sales > Leads & Opportunities*.
* Configure the available sources and campaigns from the menus there.

Usage
=====

To use this module, you need to:

#. Go to *Sales > Leads > Create*.
#. Fill the required fields.
#. Go to *Extra Info > Marketing* and fill those 3 fields.
#. *Save*.
#. *Convert to Opportunity*.
#. Choose *Opportunities > Related Customer > Create a new customer*.
#. *Create Opportunity*.
#. Click on the name of the newly linked partner.
#. Go to *Sales & Purchases*.
#. There you have the new fulfilled fields.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/9.0

Known issues / Roadmap
======================

* The new fields do not get copied to a lead object where you link the partner,
  but this is by design, because new leads from an already-existing partner not
  always come from the same campaign, source or channel.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please check there
if your issue has already been reported. If you spotted it first, help us
smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>
* Vicent Cubells <vicent.cubells@tecnativa.com>

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
