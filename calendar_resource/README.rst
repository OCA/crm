.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=================
Calendar Resource
=================

This module adds new features to facilitate resource management with meetings:

* To attach resources to a meeting, go to `Calendar` => Click on a meeting => `Edit` =>
  `Edit` => add any related resources.
* To edit or add a resource, go to `Settings` => `Resource` => `Resources`.
* This module can also prevent resources from being double-booked. Go to a resource
  and disable `Allow Double Booking` (this is enabled by default). As a note, the same
  resource in a meeting that ends at 5pm and also in a meeting that starts at 5pm on the same day
  would not not be considered double-booked.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/10.0

Known Issues / Roadmap
======================

* Tie resources into calendar types (calendar.event.type), where certain resources are available
  only with certain calendar types.
* Add a calendar view on resources, so resources such as a room can be seen if available.
* Validate Resource Leaves to avoid appointments for dates where the resource is not available.
* Validate Resource Calendar, to avoid appointments for times outside their availability.

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

* Jordi RIERA <jordi.riera@savoirfairelinux.com>
* Bruno JOLIVEAU <bruno.joliveau@savoirfairelinux.com>
* Brett Wood <bwood@laslabs.com>

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
