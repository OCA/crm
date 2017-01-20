.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Share leads with followers
==========================

It's sometimes useful to share leads with some users that would normally not have
access to them, e.g. developers for a service company so that can see and offer
their input in possibile future projects they'll have to work on.
Unfortunately the default access level on the CRM and Sale applications do not
allow for this: either a user can see all leads, or he can see only his own
leads, there is no way to "share" leads with non-sale users.

This module solves this by extending the permissions of the CRM module so that users
can be put in a group where they have (read or write) access only on leads that
were explicitly shared with them (by adding them as followers).

Configuration
=============

This module defines two additional access levels for the sale/crm application:

* See Shared Leads: users in this groups can see leads where they have been added as followers
* Edit Shared Leads: users in this groups can see and edit leads where they have been added as followers

Neither of these groups give the user the permission to create or delete leads, nor they impact
permissions on sale orders and quotations.
Users of the group 'Sale / Own Documents Only' are automatically added to the 'Edit Shared Leads' group,
that means that they will be automatically able to edit leads they are following.


Usage
=====

Add the users to the followers of the leads you want them to be able to see/edit
(according to the group you put them in).

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Leonardo Donelli @ MONK Software <leonardo.donelli@monksoftware.it>

Funders
-------

The development of this module has been financially supported by:

* MONK Software

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
