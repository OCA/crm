.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3
Restrict follower selection
===========================

This module was written to allow you to restrict the selection of possible followers. For example, if you use the social ERP functions only internally, it makes sense to filter possible followers for being employees. Otherwise, you'll get a quite crowded list of partners to choose from.

Configuration
=============

To configure this module, you need to go to `System parameters` and adjust `mail_restrict_follower_selection.domain` as you see fit. This restricts followers globally, if you want to restrict only the followers for a certain record type (or have different restrictions for different record types), create a parameter `mail_restrict_follower_selection.domain.$your_model`.

Note: This module won't change existing followers!

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/crm/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/crm/issues/new?body=module:%20mail_restrict_follower_selection%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>

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
