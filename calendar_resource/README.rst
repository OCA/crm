.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=================
Calendar Resource
=================

This module adds new features to facilitate resource management with meetings:

* To attach resources to a meeting, go to `Calendar` => Click on a meeting => `Edit` =>
  `Edit` => add any related resources.
* To edit or add a resource, go to `Calendar` => `Resources` => `Resources`.
* This module can also prevent resources from being double-booked. Go to a resource
  and disable or enable `Allow Double Booking` (this is disabled by default). As a note, the same
  resource in a meeting that ends at 5pm and in a meeting that starts at 5pm on the same day
  would not not be considered double-booked.
* You can restrict resources to certain calendar types. In the Resources form view, edit the
  `Event Types` field. The resource can then be added to events only of those types.
* Resources cannot be added to events when they're not available, either because they're on leave
  or because the event time is outside their working time.
* If you have an event selected as `allday`, only if there are no working times available
  on 1 or more of the days in that event will an error be raised. For example, if you set
  an event to `allday` on a Saturday and there are no working times at all that Saturday
  for a particular resource, then an error will be raised. However, if there is at least
  1 working time interval for that resource on the Saturday, regardless of how long or
  short that working time is, the day will be considered covered by that working time.
  If the event is not `allday`, any time the resource is not available during the event,
  regardless of the time of day, will cause an error to be raised.
* To stop leaves and working time validations on a resource when adding to an event,
  set the resource's `Working Time` field to blank in the resource form view.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/10.0

Roadmap
=======

* Abstract out logic from _check_resource_ids_working_times into separate methods in
  resource.calendar.

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
