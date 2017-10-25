.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=================
Phonecall planner
=================

Use this module to plan a phone calls schedule for your partners, assuming you
have specified the ideal time to call them.

Configuration
=============

To use this module, you need to specify your partners' preferred phone call
schedule:

#. Go to any partner's form > *Phone Calls*.
#. Set the preferred phone calling schedule for the partner.
#. Repeat above steps for all of your partners.

Usage
=====

Now, to actually generate the phone call planning:

#. Go to *Sales > Phone Calls > Planner*.
#. Fill the fields under *Call details*. Those fields will be saved literally
   in the generated phone calls.
#. Fill the fields under *Criteria*. Those fields are used to filter the
   partners and the preexisting calls. The UTM fields will also be saved
   literally in the generated phone calls.
#. Fill the fields under *Times*. See note below.
#. Fill the fields under *Repetition*. See note below.
#. Press *Generate planning*.
#. Wait a little bit (this is usually a long process).
#. You will get to the list of planned phone calls. Start calling!

Note about *Times* section
--------------------------

The *Start* and *End* times behave in a special way:

* Their *date* part is used to know the start and end dates for the planning.
* Their *time* part is used to know the time at which we will plan calls *each
  day under the date range*.

The *Call duration* field indicates the time spacing you want to leave between
one call and the next one.

So, for instance, if you select start on *2017-09-01 09:00:00*, end on
*2017-09-03 10:00:00* and duration of *1:00*, it will try to generate these
phone calls:

* 2017-09-01 09:00:00
* 2017-09-01 10:00:00
* 2017-09-02 09:00:00
* 2017-09-02 10:00:00
* 2017-09-03 09:00:00
* 2017-09-03 10:00:00

Note about *Repetition* section
-------------------------------

If you choose not to repeat calls, the planner will try to schedule one single
phone call for each **criteria combination** (*Partner + Campaign + Source +
Medium*) under the specified conditions in the *Times* section (see note above).

If you choose instead to repeat calls after some amount of days (*Days gap*),
the planner will:

#. Try to find a partner that matches the **criteria combination** and has never
   been called; then schedule a call for him.
#. If all matching partners have already been called, then search for matching
   partners that have not been called in the specified *Days gap*; then schedule a
   call for the one with least total scheduled calls.
#. If there is still no match, then schedule nothing and continue.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/9.0

Known issues / Roadmap
======================

* Incompatible with ``crm_phonecall_summary_predefined`` addon.

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

* `Tecnativa <https://www.tecnativa.com>`_:
  * Jairo Llopis <jairo.llopis@tecnativa.com>

Do not contact contributors directly about support or help with technical issues.

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
